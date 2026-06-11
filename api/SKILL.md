---
name: api
description: Generate RESTful API endpoint code including controller, service, repository, entity, and DTO layers. Use when the user wants to create a new API, endpoint, or interface.
disable-model-invocation: true
---

Create a RESTful API endpoint based on the following requirements:

$ARGUMENTS

## Instructions

1. First analyze the existing project structure, framework (Spring Boot / Express / Django / etc.), and coding conventions
2. Generate code following the project's established patterns

## Code generation layers

Generate the following layers as needed:

### 1. Entity / Model
- Database entity mapping
- Field validation annotations
- Proper data types

### 2. DTO (Request / Response)
- Request DTO with validation
- Response DTO (no sensitive fields)

### 3. Repository / DAO
- Data access methods
- Custom queries if needed

### 4. Service
- Business logic
- Transaction management
- Error handling

### 5. Controller
- RESTful URL conventions (GET/POST/PUT/DELETE)
- Request validation
- Proper HTTP status codes
- Swagger/OpenAPI annotations if the project uses them

## Principles
- Follow existing project conventions and package structure
- Include proper error handling
- Add input validation
- Use appropriate HTTP status codes
- Keep it consistent with existing code style
