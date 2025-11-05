# Dukan: Intelligent E-commerce Backend

Dukan is a powerful and feature-rich e-commerce backend built with Python and Django. It's designed to provide a solid foundation for online stores, incorporating modern development practices and advanced, data-driven features to enhance the user experience.

LIVE: https://mini-com-ngdx.onrender.com

## Key Features

1.  **Intelligent Product Search:**
    The search functionality is enhanced with typo-tolerance and auto-correction using `SymSpell`. This ensures users can find products even if they make spelling mistakes. Future plans include implementing search by image to further improve product discovery.

2.  **Recommendation Engine:**
    The platform includes a "Frequently Bought Together" feature, powered by collaborative filtering algorithms. This helps increase sales and improve user engagement by suggesting relevant products based on the purchasing patterns of other customers.

3.  **Comprehensive E-commerce API:**
    A complete RESTful API built with Django REST Framework provides all necessary endpoints for managing products, carts, orders, and users. Authentication is handled securely using JWT (JSON Web Tokens).

4.  **Scalable and Robust Architecture:**
    The project is built for performance and scalability. It utilizes Redis for caching (e.g., caching the spell-check dictionary), PostgreSQL as the primary database, and Gunicorn for production deployment, ensuring a reliable and efficient service.


## TODO
- [ ] Implement search by image.
- [ ] Cache the SymSpell dictionary to improve search performance.
- [ ] Allow modification of ordered items with custom product details.
- [ ] Refine and expand the recommendation models.
