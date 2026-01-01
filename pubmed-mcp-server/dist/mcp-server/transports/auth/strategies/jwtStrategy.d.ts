import type { AuthInfo } from "../lib/authTypes.js";
import type { AuthStrategy } from "./authStrategy.js";
export declare class JwtStrategy implements AuthStrategy {
    private readonly secretKey;
    constructor();
    verify(token: string): Promise<AuthInfo>;
}
//# sourceMappingURL=jwtStrategy.d.ts.map