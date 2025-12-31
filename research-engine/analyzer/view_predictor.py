#!/usr/bin/env python3
"""
View Predictor - Predict video performance based on topic + modifiers

Uses historical data from scraped videos to predict views for new topic combinations.

Model: Simple regression on features extracted from title/topic patterns.
As data grows, can upgrade to more sophisticated ML models.

Usage:
    python view_predictor.py "Apo B" "Women 45-65" "Myth-Busting"
    python view_predictor.py --train                    # Retrain model on latest data
    python view_predictor.py --evaluate                 # Show model performance
"""

import json
import re
import pickle
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import argparse

try:
    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import cross_val_score
except ImportError:
    import os
    os.system("pip install numpy scikit-learn")
    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import cross_val_score

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SCRAPED_DIR = DATA_DIR / "scraped"
MODEL_DIR = DATA_DIR / "models"


class ViewPredictor:
    """Predicts video views based on topic and content features."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        self.model = Ridge(alpha=1.0)
        self.is_trained = False
        self.training_stats = {}

    def _extract_features(self, title, additional_text=""):
        """Extract features from video title and metadata."""
        combined = f"{title} {additional_text}".lower()
        return combined

    def train(self, videos):
        """Train the model on scraped video data."""
        if len(videos) < 10:
            print("Need at least 10 videos to train. Scrape more data.")
            return False

        # Prepare training data
        texts = []
        views = []

        for video in videos:
            title = video.get("title", "")
            channel = video.get("channel_name", "")
            niche = video.get("channel_niche", "")
            view_count = video.get("views", 0)

            if title and view_count > 0:
                feature_text = self._extract_features(title, f"{channel} {niche}")
                texts.append(feature_text)
                views.append(np.log1p(view_count))  # Log transform views

        if len(texts) < 10:
            print("Not enough valid videos with views.")
            return False

        # Fit vectorizer and model
        X = self.vectorizer.fit_transform(texts)
        y = np.array(views)

        # Cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5, scoring='r2')

        # Train on full data
        self.model.fit(X, y)
        self.is_trained = True

        # Store training stats
        self.training_stats = {
            "n_samples": len(texts),
            "cv_r2_mean": float(np.mean(cv_scores)),
            "cv_r2_std": float(np.std(cv_scores)),
            "trained_at": datetime.now().isoformat(),
            "view_range": {
                "min": int(np.expm1(min(views))),
                "max": int(np.expm1(max(views))),
                "median": int(np.expm1(np.median(views)))
            }
        }

        print(f"Model trained on {len(texts)} videos")
        print(f"Cross-validation R²: {self.training_stats['cv_r2_mean']:.3f} ± {self.training_stats['cv_r2_std']:.3f}")

        return True

    def predict(self, seed_idea, modifier="", angle=""):
        """Predict views for a topic combination."""
        if not self.is_trained:
            return {"error": "Model not trained. Run with --train first."}

        # Construct hypothetical title
        if modifier and angle:
            query = f"{seed_idea} {modifier} {angle}"
        elif modifier:
            query = f"{seed_idea} {modifier}"
        else:
            query = seed_idea

        # Transform and predict
        X = self.vectorizer.transform([query.lower()])
        log_views = self.model.predict(X)[0]
        predicted_views = int(np.expm1(log_views))

        # Calculate confidence based on training data range
        median_views = self.training_stats["view_range"]["median"]
        confidence = min(1.0, self.training_stats["cv_r2_mean"] + 0.2)

        # Estimate range (±1 std from historical)
        low_estimate = int(predicted_views * 0.5)
        high_estimate = int(predicted_views * 2.0)

        return {
            "query": query,
            "predicted_views": predicted_views,
            "confidence": round(confidence, 2),
            "range": {
                "low": low_estimate,
                "high": high_estimate
            },
            "comparison_to_median": round(predicted_views / median_views, 2) if median_views > 0 else 1.0,
            "recommendation": self._get_recommendation(predicted_views, median_views)
        }

    def _get_recommendation(self, predicted, median):
        """Generate recommendation based on prediction."""
        ratio = predicted / median if median > 0 else 1.0
        if ratio > 1.5:
            return "HIGH POTENTIAL - Strong topic, prioritize this"
        elif ratio > 1.0:
            return "GOOD - Above average expected performance"
        elif ratio > 0.5:
            return "MODERATE - Average performance expected"
        else:
            return "LOW - Consider different angle or modifier"

    def save(self, path=None):
        """Save trained model to disk."""
        if not path:
            MODEL_DIR.mkdir(exist_ok=True)
            path = MODEL_DIR / "view_predictor.pkl"

        with open(path, "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "model": self.model,
                "is_trained": self.is_trained,
                "training_stats": self.training_stats
            }, f)
        print(f"Model saved to: {path}")

    def load(self, path=None):
        """Load trained model from disk."""
        if not path:
            path = MODEL_DIR / "view_predictor.pkl"

        if not path.exists():
            return False

        with open(path, "rb") as f:
            data = pickle.load(f)
            self.vectorizer = data["vectorizer"]
            self.model = data["model"]
            self.is_trained = data["is_trained"]
            self.training_stats = data.get("training_stats", {})

        return True


def load_videos():
    """Load latest scraped videos."""
    latest_file = SCRAPED_DIR / "latest_scrape.json"
    if not latest_file.exists():
        return []

    with open(latest_file, "r") as f:
        meta = json.load(f)

    videos_file = Path(meta["file"])
    if not videos_file.exists():
        return []

    with open(videos_file, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Predict video views for topic combinations")
    parser.add_argument("topics", nargs="*", help="Topic + modifier + angle to predict")
    parser.add_argument("--train", action="store_true", help="Train model on scraped data")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate model performance")
    args = parser.parse_args()

    predictor = ViewPredictor()

    if args.train:
        print("Loading scraped videos...")
        videos = load_videos()
        if not videos:
            print("No videos found. Run channel_scraper.py first.")
            return

        print(f"Training on {len(videos)} videos...")
        if predictor.train(videos):
            predictor.save()
            print("\nModel trained and saved!")
            print(f"\nTraining stats:")
            for k, v in predictor.training_stats.items():
                print(f"  {k}: {v}")
        return

    if args.evaluate:
        if not predictor.load():
            print("No trained model found. Run with --train first.")
            return

        print("Model Evaluation:")
        for k, v in predictor.training_stats.items():
            print(f"  {k}: {v}")
        return

    # Prediction mode
    if not args.topics:
        print("Usage: python view_predictor.py 'Apo B' 'Women 45-65' 'Myth-Busting'")
        print("       python view_predictor.py --train")
        return

    if not predictor.load():
        print("No trained model found. Run with --train first.")
        return

    # Parse topics
    seed_idea = args.topics[0] if len(args.topics) > 0 else ""
    modifier = args.topics[1] if len(args.topics) > 1 else ""
    angle = args.topics[2] if len(args.topics) > 2 else ""

    result = predictor.predict(seed_idea, modifier, angle)

    print(f"\n{'='*60}")
    print("VIEW PREDICTION")
    print(f"{'='*60}")
    print(f"Query: {result['query']}")
    print(f"\nPredicted Views: {result['predicted_views']:,}")
    print(f"Confidence: {result['confidence']}")
    print(f"Range: {result['range']['low']:,} - {result['range']['high']:,}")
    print(f"vs Median: {result['comparison_to_median']}x")
    print(f"\nRecommendation: {result['recommendation']}")


if __name__ == "__main__":
    main()
