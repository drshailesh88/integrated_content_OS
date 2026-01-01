/**
 * @fileoverview Abstract base class for transport managers.
 * @module src/mcp-server/transports/core/baseTransportManager
 */
import { logger, requestContextService, } from "../../../utils/index.js";
/**
 * Abstract base class for transport managers, providing common functionality.
 */
export class BaseTransportManager {
    createServerInstanceFn;
    constructor(createServerInstanceFn) {
        const context = requestContextService.createRequestContext({
            operation: "BaseTransportManager.constructor",
            managerType: this.constructor.name,
        });
        logger.debug("Initializing transport manager.", context);
        this.createServerInstanceFn = createServerInstanceFn;
    }
}
//# sourceMappingURL=baseTransportManager.js.map