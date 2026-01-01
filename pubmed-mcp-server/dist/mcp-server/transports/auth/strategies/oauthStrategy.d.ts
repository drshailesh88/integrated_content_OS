import type { AuthInfo } from "../lib/authTypes.js";
import type { AuthStrategy } from "./authStrategy.js";
export declare class OauthStrategy implements AuthStrategy {
    private readonly jwks;
    constructor();
    verify(token: string): Promise<AuthInfo>;
}
//# sourceMappingURL=oauthStrategy.d.ts.map