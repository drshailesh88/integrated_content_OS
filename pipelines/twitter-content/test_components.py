#!/usr/bin/env python3
"""
Component Testing Script
Tests each part of the system individually with minimal API usage.
"""

import asyncio
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, '.')


def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_result(success: bool, message: str):
    icon = "✓" if success else "✗"
    print(f"  {icon} {message}")


async def test_config():
    """Test 1: Configuration loading"""
    print_header("TEST 1: Configuration")

    try:
        from src.config import config

        # Check each component
        print_result(bool(config.apify.api_key), f"Apify API key: {'configured' if config.apify.api_key else 'MISSING'}")
        print_result(bool(config.llm.openrouter_api_key or config.llm.anthropic_api_key),
                    f"LLM API key: {'OpenRouter' if config.llm.openrouter_api_key else 'Anthropic' if config.llm.anthropic_api_key else 'MISSING'}")
        print_result(bool(config.openai.api_key), f"OpenAI API key: {'configured' if config.openai.api_key else 'MISSING'}")
        print_result(bool(config.astradb.api_endpoint), f"AstraDB endpoint: {'configured' if config.astradb.api_endpoint else 'MISSING'}")
        print_result(bool(config.astradb.application_token), f"AstraDB token: {'configured' if config.astradb.application_token else 'MISSING'}")

        # Show collection name
        print(f"\n  AstraDB collection: {config.astradb.collection_name}")
        print(f"  Inspiration accounts: {len(config.apify.max_tweets_per_account)} configured")

        issues = config.validate()
        if issues:
            print(f"\n  ⚠️  Issues: {', '.join(issues)}")
            return False

        print("\n  ✓ Configuration OK")
        return True

    except Exception as e:
        print_result(False, f"Config error: {e}")
        return False


async def test_pubmed():
    """Test 2: PubMed API (free, no credits)"""
    print_header("TEST 2: PubMed API")

    try:
        from src.utils.pubmed import pubmed_client

        # Simple search - uses free NCBI API
        print("  Searching PubMed for 'SGLT2 heart failure'...")
        pmids = await pubmed_client.search(
            query="SGLT2 inhibitors heart failure",
            max_results=3,
            filter_q1_journals=True,
        )

        print_result(len(pmids) > 0, f"Found {len(pmids)} PMIDs: {pmids}")

        if pmids:
            # Fetch one article
            print("  Fetching article details...")
            articles = await pubmed_client.fetch_articles(pmids[:1])

            if articles:
                article = articles[0]
                print_result(True, f"Article: {article.title[:60]}...")
                print(f"      Journal: {article.journal} ({article.year})")
                print(f"      Q1 Journal: {article.is_q1_journal}")
                print(f"      Citation: {article.get_citation()}")
                return True

        return len(pmids) > 0

    except Exception as e:
        print_result(False, f"PubMed error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_astradb():
    """Test 3: AstraDB connection (1 query)"""
    print_header("TEST 3: AstraDB Connection")

    try:
        from src.config import config

        if not config.astradb.api_endpoint or not config.astradb.application_token:
            print_result(False, "AstraDB not configured - skipping")
            return False

        from src.utils.astradb import astradb_client

        # Test with a simple query (uses 1 embedding call)
        print(f"  Collection: {config.astradb.collection_name}")
        print("  Testing connection with simple query...")
        print("  (This will use 1 OpenAI embedding call)")

        # Use a simple query without HyDE to minimize LLM usage
        results = await astradb_client.query(
            query="heart failure guidelines",
            use_hyde=False,  # Skip HyDE to save LLM call
            top_k=3,
        )

        print_result(len(results) > 0, f"Found {len(results)} results")

        if results:
            for i, r in enumerate(results[:2], 1):
                print(f"\n  Result {i}:")
                print(f"    Source: {r.source_name}")
                print(f"    Type: {r.source_type}")
                print(f"    Similarity: {r.similarity:.2%}")
                print(f"    Content: {r.content[:100]}...")

        return len(results) > 0

    except Exception as e:
        print_result(False, f"AstraDB error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_llm_minimal():
    """Test 4: LLM API (minimal prompt)"""
    print_header("TEST 4: LLM API (Minimal)")

    try:
        from src.utils.llm import llm_client

        # Super minimal prompt to test connectivity
        print("  Testing LLM with minimal prompt...")
        print("  (This will use ~50 tokens)")

        response = await llm_client.generate(
            prompt="Reply with only: 'API working'",
            max_tokens=10,
            temperature=0,
        )

        print_result("working" in response.lower(), f"Response: {response.strip()}")
        return "working" in response.lower()

    except Exception as e:
        print_result(False, f"LLM error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_embedding():
    """Test 5: OpenAI Embedding"""
    print_header("TEST 5: OpenAI Embedding")

    try:
        from src.utils.llm import llm_client

        print("  Testing embedding generation...")
        print("  (This will use 1 embedding call)")

        embedding = await llm_client.get_embedding("heart failure treatment")

        print_result(len(embedding) == 1536, f"Embedding dimensions: {len(embedding)}")
        print(f"    First 5 values: {embedding[:5]}")

        return len(embedding) == 1536

    except Exception as e:
        print_result(False, f"Embedding error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_harvester_mock():
    """Test 6: Harvester (mock, no Apify)"""
    print_header("TEST 6: Harvester (Mock)")

    try:
        from src.harvester import IdeaHarvester
        from src.utils.apify import Tweet
        from datetime import datetime

        harvester = IdeaHarvester()

        # Create a mock tweet
        mock_tweet = Tweet(
            id="test123",
            text="Fascinating new data on SGLT2 inhibitors showing benefits even in HFpEF patients with preserved EF >50%. The mechanism appears to be independent of glucose lowering.",
            url="https://twitter.com/test/status/123",
            author_handle="TestDoctor",
            author_name="Test Doctor MD",
            created_at=datetime.now(),
            likes=500,
            retweets=100,
            replies=50,
        )

        print("  Testing idea extraction from mock tweet...")
        print(f"    Tweet: {mock_tweet.text[:60]}...")
        print("  (This will use 1 LLM call)")

        idea = await harvester._extract_idea_from_tweet(mock_tweet, 1)

        if idea:
            print_result(True, "Idea extracted successfully")
            print(f"\n    Research Question: {idea.research_question}")
            print(f"    PubMed Query: {idea.pubmed_query}")
            print(f"    RAG Keywords: {idea.rag_keywords}")
            print(f"    Category: {idea.topic_category}")
            return True
        else:
            print_result(False, "Failed to extract idea")
            return False

    except Exception as e:
        print_result(False, f"Harvester error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_synthesizer_mock():
    """Test 7: Synthesizer (mock data)"""
    print_header("TEST 7: Synthesizer (Mock)")

    try:
        from src.synthesizer import KnowledgeSynthesizer
        from src.researcher import ResearchResults
        from src.harvester import ContentIdea
        from src.utils.pubmed import PubMedArticle
        from src.utils.astradb import RAGResult
        from src.utils.apify import Tweet
        from datetime import datetime

        synthesizer = KnowledgeSynthesizer()

        # Create mock data
        mock_tweet = Tweet(
            id="test", text="SGLT2 test", url="", author_handle="test",
            author_name="Test", created_at=datetime.now(), likes=0, retweets=0, replies=0
        )

        mock_idea = ContentIdea(
            id="test-001",
            original_tweet=mock_tweet,
            research_question="What is the evidence for SGLT2 inhibitors in HFpEF?",
            pubmed_query="SGLT2 HFpEF",
            rag_keywords=["SGLT2", "HFpEF", "dapagliflozin"],
            topic_category="heart_failure",
            engagement_score=100,
        )

        mock_articles = [
            PubMedArticle(
                pmid="12345678",
                title="DELIVER Trial: Dapagliflozin in HFpEF",
                abstract="DELIVER randomized 6263 patients with HFpEF to dapagliflozin or placebo. Primary outcome was cardiovascular death or worsening HF. Dapagliflozin reduced risk by 18% (HR 0.82, 95% CI 0.73-0.92).",
                authors=["Solomon SD", "McMurray JJV"],
                journal="N Engl J Med",
                year="2022",
                doi="10.1056/NEJMoa2206286",
                is_q1_journal=True,
            )
        ]

        mock_rag = [
            RAGResult(
                content="The ACC/AHA guidelines recommend SGLT2 inhibitors for patients with heart failure regardless of ejection fraction (Class 1, Level A).",
                source_name="ACC/AHA Heart Failure Guidelines 2022",
                source_type="guideline",
                chapter="Pharmacotherapy",
                similarity=0.89,
            )
        ]

        mock_research = ResearchResults(
            idea=mock_idea,
            pubmed_articles=mock_articles,
            rag_results=mock_rag,
        )

        print("  Testing synthesis with mock research data...")
        print("  (This will use 1 LLM call)")

        brief = await synthesizer.synthesize(mock_research)

        print_result(bool(brief.executive_summary), "Brief generated")
        print(f"\n  Executive Summary:\n    {brief.executive_summary[:200]}...")
        print(f"\n  Content Angles: {brief.content_angles}")
        print(f"  Citations: {len(brief.citations)}")

        return bool(brief.executive_summary)

    except Exception as e:
        print_result(False, f"Synthesizer error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_writer_mock():
    """Test 8: Writer (mock brief)"""
    print_header("TEST 8: Content Writer (Mock)")

    try:
        from src.writer import ContentWriter, ContentFormat
        from src.synthesizer import KnowledgeBrief

        writer = ContentWriter()

        # Create mock brief
        mock_brief = KnowledgeBrief(
            idea_id="test-001",
            research_question="What is the evidence for SGLT2 inhibitors in HFpEF?",
            executive_summary="SGLT2 inhibitors reduce cardiovascular death and heart failure hospitalization in HFpEF, as demonstrated by DELIVER and EMPEROR-Preserved trials.",
            key_evidence="- DELIVER (NEJM 2022): 18% reduction in primary outcome (HR 0.82)\n- EMPEROR-Preserved: Similar benefits with empagliflozin",
            guideline_perspective="ACC/AHA recommends SGLT2i for HF regardless of EF (Class 1, Level A)",
            nuances_controversies="Mechanism in HFpEF not fully understood; benefits appear independent of glucose lowering",
            content_angles=[
                "The HFpEF breakthrough we've been waiting for",
                "Why SGLT2 inhibitors work even without diabetes",
                "DELIVER changes the treatment paradigm"
            ],
            citations=[
                "Solomon SD et al. N Engl J Med. 2022 (DELIVER)",
                "Anker SD et al. N Engl J Med. 2021 (EMPEROR-Preserved)"
            ],
            raw_synthesis="Full synthesis text here...",
        )

        print("  Testing content generation (tweet format)...")
        print("  (This will use 1 LLM call)")

        content = await writer.write(mock_brief, format=ContentFormat.TWEET)

        print_result(len(content.content) <= 300, f"Tweet generated ({len(content.content)} chars)")
        print(f"\n  Content:\n    {content.content}")

        return len(content.content) > 0

    except Exception as e:
        print_result(False, f"Writer error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all component tests."""
    print("\n" + "="*60)
    print("  TWITTER CONTENT SYSTEM - COMPONENT TESTS")
    print("="*60)
    print("\nThis will test each component with minimal API usage.")
    print("Estimated cost: ~$0.01-0.02 (few LLM calls + embeddings)")

    results = {}

    # Test 1: Config (no API)
    results['config'] = await test_config()

    if not results['config']:
        print("\n⚠️  Fix configuration before continuing.")
        return results

    # Test 2: PubMed (free API)
    results['pubmed'] = await test_pubmed()

    # Test 3: AstraDB (1 embedding)
    results['astradb'] = await test_astradb()

    # Test 4: LLM minimal
    results['llm'] = await test_llm_minimal()

    if not results['llm']:
        print("\n⚠️  LLM not working. Skipping remaining tests.")
        return results

    # Test 5: Embedding
    results['embedding'] = await test_embedding()

    # Test 6: Harvester with mock tweet
    results['harvester'] = await test_harvester_mock()

    # Test 7: Synthesizer with mock data
    results['synthesizer'] = await test_synthesizer_mock()

    # Test 8: Writer with mock brief
    results['writer'] = await test_writer_mock()

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, passed_test in results.items():
        print_result(passed_test, name.upper())

    print(f"\n  {passed}/{total} tests passed")

    if passed == total:
        print("\n  🎉 All components working! Ready for full pipeline test.")
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"\n  ⚠️  Failed: {', '.join(failed)}")

    return results


if __name__ == "__main__":
    asyncio.run(run_all_tests())
