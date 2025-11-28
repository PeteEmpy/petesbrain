import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";
import { z } from "zod";

// Initialize MCP server
const server = new McpServer({
  name: "WooCommerce Service",
  version: "2.0.0",
});

// WooCommerce API configuration
const woocommerceConfig = {
  url: process.env.WOOCOMMERCE_URL || 'https://your-store.com',
  consumerKey: process.env.WOOCOMMERCE_CONSUMER_KEY || 'your-consumer-key',
  consumerSecret: process.env.WOOCOMMERCE_CONSUMER_SECRET || 'your-consumer-secret',
  version: 'wc/v3'
};

/**
 * Helper function to make WooCommerce API requests
 * @param {string} endpoint - The API endpoint
 * @param {Object} params - Query parameters
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {Object} data - Request body data
 * @returns {Promise<Object>} - Response data
 */
async function makeWooCommerceRequest(endpoint, params = {}, method = 'GET', data = null) {
  try {
    const config = {
      method,
      url: `${woocommerceConfig.url}/wp-json/${woocommerceConfig.version}/${endpoint}`,
      params,
      auth: {
        username: woocommerceConfig.consumerKey,
        password: woocommerceConfig.consumerSecret
      }
    };

    if (data && (method === 'POST' || method === 'PUT')) {
      config.data = data;
    }

    const response = await axios(config);
    return response.data;
  } catch (error) {
    console.error('Error making WooCommerce request:', error.message);
    throw new Error(`Failed to fetch data from WooCommerce: ${error.message}`);
  }
}

/**
 * Format an order into a readable string
 */
function formatOrder(order) {
  const items = order.line_items.map(item =>
    `- ${item.quantity}x ${item.name} (${item.price})`
  ).join('\n');

  return `
Order #${order.id}
Date: ${new Date(order.date_created).toLocaleString()}
Status: ${order.status}
Customer: ${order.billing.first_name} ${order.billing.last_name} (${order.billing.email})
Total: ${order.total} ${order.currency}

Items:
${items}

Shipping Address:
${order.shipping.first_name} ${order.shipping.last_name}
${order.shipping.address_1}
${order.shipping.city}, ${order.shipping.state} ${order.shipping.postcode}
${order.shipping.country}
`;
}

/**
 * Format a product into a readable string
 */
function formatProduct(product) {
  const categories = product.categories ? product.categories.map(cat => cat.name).join(', ') : 'N/A';
  const tags = product.tags ? product.tags.map(tag => tag.name).join(', ') : 'N/A';

  return `
Product ID: ${product.id}
Name: ${product.name}
SKU: ${product.sku || 'N/A'}
Price: ${product.price}
Regular Price: ${product.regular_price}
Sale Price: ${product.sale_price || 'N/A'}
Stock Status: ${product.stock_status}
Stock Quantity: ${product.stock_quantity || 'N/A'}
Categories: ${categories}
Tags: ${tags}
Type: ${product.type}
Status: ${product.status}
`;
}

/**
 * Format a customer into a readable string
 */
function formatCustomer(customer) {
  return `
Customer ID: ${customer.id}
Name: ${customer.first_name} ${customer.last_name}
Email: ${customer.email}
Username: ${customer.username || 'N/A'}
Orders Count: ${customer.orders_count || 0}
Total Spent: ${customer.total_spent || 0}
Billing Address: ${customer.billing.city}, ${customer.billing.state} ${customer.billing.postcode}, ${customer.billing.country}
Date Created: ${new Date(customer.date_created).toLocaleString()}
`;
}

/**
 * Format a category into a readable string
 */
function formatCategory(category) {
  return `
Category ID: ${category.id}
Name: ${category.name}
Slug: ${category.slug}
Parent ID: ${category.parent || 'None'}
Description: ${category.description || 'N/A'}
Count: ${category.count} products
`;
}

/**
 * Format a tag into a readable string
 */
function formatTag(tag) {
  return `
Tag ID: ${tag.id}
Name: ${tag.name}
Slug: ${tag.slug}
Description: ${tag.description || 'N/A'}
Count: ${tag.count} products
`;
}

/**
 * Format a coupon into a readable string
 */
function formatCoupon(coupon) {
  return `
Coupon ID: ${coupon.id}
Code: ${coupon.code}
Discount Type: ${coupon.discount_type}
Amount: ${coupon.amount}
Expiry Date: ${coupon.date_expires || 'No expiry'}
Usage Count: ${coupon.usage_count}
Usage Limit: ${coupon.usage_limit || 'Unlimited'}
Description: ${coupon.description || 'N/A'}
`;
}

// ========================================
// ORDERS
// ========================================

server.tool(
  "getRecentOrders",
  {
    status: z.string().optional().describe("Filter orders by status (e.g., processing, completed, on-hold)"),
    limit: z.number().optional().describe("Number of orders to return (use 0 for unlimited)"),
    after: z.string().optional().describe("Get orders after this date (format: YYYY-MM-DD)"),
    before: z.string().optional().describe("Get orders before this date (format: YYYY-MM-DD)")
  },
  async ({ status, limit, after, before }) => {
    const queryParams = {};

    if (limit && limit > 0) {
      queryParams.per_page = limit;
    }

    if (status) {
      queryParams.status = status;
    }

    if (after) {
      const afterDate = new Date(after);
      if (!isNaN(afterDate.getTime())) {
        queryParams.after = afterDate.toISOString();
      }
    }

    if (before) {
      const beforeDate = new Date(before);
      if (!isNaN(beforeDate.getTime())) {
        queryParams.before = beforeDate.toISOString();
      }
    }

    try {
      console.error(`Fetching orders with parameters:`, JSON.stringify(queryParams));
      const orders = await makeWooCommerceRequest('orders', queryParams);

      if (!orders || orders.length === 0) {
        return {
          content: [{ type: "text", text: "No orders found matching your criteria." }]
        };
      }

      const formattedOrders = orders.map(formatOrder);
      return {
        content: [{ type: "text", text: formattedOrders.join('\n\n---\n\n') }]
      };
    } catch (error) {
      console.error(`Error in getRecentOrders: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching orders: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "getOrderById",
  {
    id: z.number().describe("The order ID")
  },
  async ({ id }) => {
    try {
      console.error(`Fetching order with ID: ${id}`);
      const order = await makeWooCommerceRequest(`orders/${id}`);
      return {
        content: [{ type: "text", text: formatOrder(order) }]
      };
    } catch (error) {
      console.error(`Error in getOrderById: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching order #${id}: ${error.message}` }]
      };
    }
  }
);

// ========================================
// PRODUCTS
// ========================================

server.tool(
  "getProducts",
  {
    search: z.string().optional().describe("Search products by name or description"),
    category: z.string().optional().describe("Filter by category slug or ID"),
    tag: z.string().optional().describe("Filter by tag slug or ID"),
    limit: z.number().optional().describe("Number of products to return (default: 100)"),
    sku: z.string().optional().describe("Filter by SKU"),
    status: z.string().optional().describe("Filter by status (publish, draft, pending)"),
    type: z.string().optional().describe("Filter by product type (simple, grouped, external, variable)")
  },
  async ({ search, category, tag, limit, sku, status, type }) => {
    const queryParams = { per_page: limit || 100 };

    if (search) queryParams.search = search;
    if (category) queryParams.category = category;
    if (tag) queryParams.tag = tag;
    if (sku) queryParams.sku = sku;
    if (status) queryParams.status = status;
    if (type) queryParams.type = type;

    try {
      console.error(`Fetching products with parameters:`, JSON.stringify(queryParams));
      const products = await makeWooCommerceRequest('products', queryParams);

      if (!products || products.length === 0) {
        return {
          content: [{ type: "text", text: "No products found matching your criteria." }]
        };
      }

      const formattedProducts = products.map(formatProduct);
      return {
        content: [{ type: "text", text: formattedProducts.join('\n\n---\n\n') }]
      };
    } catch (error) {
      console.error(`Error in getProducts: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching products: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "getProductById",
  {
    id: z.number().describe("The product ID")
  },
  async ({ id }) => {
    try {
      console.error(`Fetching product with ID: ${id}`);
      const product = await makeWooCommerceRequest(`products/${id}`);
      return {
        content: [{ type: "text", text: formatProduct(product) }]
      };
    } catch (error) {
      console.error(`Error in getProductById: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching product #${id}: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "getProductVariations",
  {
    product_id: z.number().describe("The parent product ID"),
    limit: z.number().optional().describe("Number of variations to return (default: 100)")
  },
  async ({ product_id, limit }) => {
    const queryParams = { per_page: limit || 100 };

    try {
      console.error(`Fetching variations for product ID: ${product_id}`);
      const variations = await makeWooCommerceRequest(`products/${product_id}/variations`, queryParams);

      if (!variations || variations.length === 0) {
        return {
          content: [{ type: "text", text: "No variations found for this product." }]
        };
      }

      const formattedVariations = variations.map(v => `
Variation ID: ${v.id}
SKU: ${v.sku || 'N/A'}
Price: ${v.price}
Stock Status: ${v.stock_status}
Stock Quantity: ${v.stock_quantity || 'N/A'}
Attributes: ${v.attributes.map(a => `${a.name}: ${a.option}`).join(', ')}
`).join('\n---\n');

      return {
        content: [{ type: "text", text: formattedVariations }]
      };
    } catch (error) {
      console.error(`Error in getProductVariations: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching variations: ${error.message}` }]
      };
    }
  }
);

// ========================================
// CATEGORIES
// ========================================

server.tool(
  "getProductCategories",
  {
    limit: z.number().optional().describe("Number of categories to return (default: 100)"),
    search: z.string().optional().describe("Search categories by name")
  },
  async ({ limit, search }) => {
    const queryParams = { per_page: limit || 100 };
    if (search) queryParams.search = search;

    try {
      console.error(`Fetching categories with parameters:`, JSON.stringify(queryParams));
      const categories = await makeWooCommerceRequest('products/categories', queryParams);

      if (!categories || categories.length === 0) {
        return {
          content: [{ type: "text", text: "No categories found." }]
        };
      }

      const formattedCategories = categories.map(formatCategory);
      return {
        content: [{ type: "text", text: formattedCategories.join('\n\n---\n\n') }]
      };
    } catch (error) {
      console.error(`Error in getProductCategories: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching categories: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "getCategoryById",
  {
    id: z.number().describe("The category ID")
  },
  async ({ id }) => {
    try {
      console.error(`Fetching category with ID: ${id}`);
      const category = await makeWooCommerceRequest(`products/categories/${id}`);
      return {
        content: [{ type: "text", text: formatCategory(category) }]
      };
    } catch (error) {
      console.error(`Error in getCategoryById: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching category #${id}: ${error.message}` }]
      };
    }
  }
);

// ========================================
// TAGS
// ========================================

server.tool(
  "getProductTags",
  {
    limit: z.number().optional().describe("Number of tags to return (default: 100)"),
    search: z.string().optional().describe("Search tags by name")
  },
  async ({ limit, search }) => {
    const queryParams = { per_page: limit || 100 };
    if (search) queryParams.search = search;

    try {
      console.error(`Fetching tags with parameters:`, JSON.stringify(queryParams));
      const tags = await makeWooCommerceRequest('products/tags', queryParams);

      if (!tags || tags.length === 0) {
        return {
          content: [{ type: "text", text: "No tags found." }]
        };
      }

      const formattedTags = tags.map(formatTag);
      return {
        content: [{ type: "text", text: formattedTags.join('\n\n---\n\n') }]
      };
    } catch (error) {
      console.error(`Error in getProductTags: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching tags: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "getTagById",
  {
    id: z.number().describe("The tag ID")
  },
  async ({ id }) => {
    try {
      console.error(`Fetching tag with ID: ${id}`);
      const tag = await makeWooCommerceRequest(`products/tags/${id}`);
      return {
        content: [{ type: "text", text: formatTag(tag) }]
      };
    } catch (error) {
      console.error(`Error in getTagById: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching tag #${id}: ${error.message}` }]
      };
    }
  }
);

// ========================================
// CUSTOMERS
// ========================================

server.tool(
  "getCustomers",
  {
    limit: z.number().optional().describe("Number of customers to return (default: 100)"),
    search: z.string().optional().describe("Search customers by name or email"),
    email: z.string().optional().describe("Filter by specific email address")
  },
  async ({ limit, search, email }) => {
    const queryParams = { per_page: limit || 100 };
    if (search) queryParams.search = search;
    if (email) queryParams.email = email;

    try {
      console.error(`Fetching customers with parameters:`, JSON.stringify(queryParams));
      const customers = await makeWooCommerceRequest('customers', queryParams);

      if (!customers || customers.length === 0) {
        return {
          content: [{ type: "text", text: "No customers found." }]
        };
      }

      const formattedCustomers = customers.map(formatCustomer);
      return {
        content: [{ type: "text", text: formattedCustomers.join('\n\n---\n\n') }]
      };
    } catch (error) {
      console.error(`Error in getCustomers: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching customers: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "getCustomerById",
  {
    id: z.number().describe("The customer ID")
  },
  async ({ id }) => {
    try {
      console.error(`Fetching customer with ID: ${id}`);
      const customer = await makeWooCommerceRequest(`customers/${id}`);
      return {
        content: [{ type: "text", text: formatCustomer(customer) }]
      };
    } catch (error) {
      console.error(`Error in getCustomerById: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching customer #${id}: ${error.message}` }]
      };
    }
  }
);

// ========================================
// COUPONS
// ========================================

server.tool(
  "getCoupons",
  {
    limit: z.number().optional().describe("Number of coupons to return (default: 100)"),
    code: z.string().optional().describe("Filter by coupon code")
  },
  async ({ limit, code }) => {
    const queryParams = { per_page: limit || 100 };
    if (code) queryParams.code = code;

    try {
      console.error(`Fetching coupons with parameters:`, JSON.stringify(queryParams));
      const coupons = await makeWooCommerceRequest('coupons', queryParams);

      if (!coupons || coupons.length === 0) {
        return {
          content: [{ type: "text", text: "No coupons found." }]
        };
      }

      const formattedCoupons = coupons.map(formatCoupon);
      return {
        content: [{ type: "text", text: formattedCoupons.join('\n\n---\n\n') }]
      };
    } catch (error) {
      console.error(`Error in getCoupons: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching coupons: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "getCouponById",
  {
    id: z.number().describe("The coupon ID")
  },
  async ({ id }) => {
    try {
      console.error(`Fetching coupon with ID: ${id}`);
      const coupon = await makeWooCommerceRequest(`coupons/${id}`);
      return {
        content: [{ type: "text", text: formatCoupon(coupon) }]
      };
    } catch (error) {
      console.error(`Error in getCouponById: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error fetching coupon #${id}: ${error.message}` }]
      };
    }
  }
);

// ========================================
// UPDATE OPERATIONS
// ========================================

server.tool(
  "updateProduct",
  {
    id: z.number().describe("The product ID to update"),
    data: z.record(z.any()).describe("Product data to update (JSON object with WooCommerce product fields)")
  },
  async ({ id, data }) => {
    try {
      console.error(`Updating product with ID: ${id}`, JSON.stringify(data));
      const product = await makeWooCommerceRequest(`products/${id}`, {}, 'PUT', data);
      return {
        content: [{ type: "text", text: `Product #${id} updated successfully:\n\n${formatProduct(product)}` }]
      };
    } catch (error) {
      console.error(`Error in updateProduct: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error updating product #${id}: ${error.message}` }]
      };
    }
  }
);

server.tool(
  "updateOrder",
  {
    id: z.number().describe("The order ID to update"),
    data: z.record(z.any()).describe("Order data to update (JSON object with WooCommerce order fields)")
  },
  async ({ id, data }) => {
    try {
      console.error(`Updating order with ID: ${id}`, JSON.stringify(data));
      const order = await makeWooCommerceRequest(`orders/${id}`, {}, 'PUT', data);
      return {
        content: [{ type: "text", text: `Order #${id} updated successfully:\n\n${formatOrder(order)}` }]
      };
    } catch (error) {
      console.error(`Error in updateOrder: ${error.message}`);
      return {
        content: [{ type: "text", text: `Error updating order #${id}: ${error.message}` }]
      };
    }
  }
);

// Start the server using the StdioServerTransport
const transport = new StdioServerTransport();
console.error('WooCommerce MCP server v2.0.0 starting...');
await server.connect(transport);
console.error('WooCommerce MCP server connected with comprehensive WooCommerce API support');
