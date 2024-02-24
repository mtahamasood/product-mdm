CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Drop tables if they exist
DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;

-- Drop type if exists
DROP TYPE IF EXISTS box_size CASCADE;

-- Create enum type for BoxSize
CREATE TYPE box_size AS ENUM ('big', 'medium', 'small');

-- Create Tenants Table
CREATE TABLE tenants (
    tenant_id SERIAL PRIMARY KEY,
    tenant_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Roles Table
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(255) UNIQUE NOT NULL
);

-- Create Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);

-- Create UserRoles Association Table
CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- Create Products Table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    product_name VARCHAR(500) NOT NULL,
    box_size box_size NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);

-- Insert sample data
-- Insert tenants
INSERT INTO tenants (tenant_name) VALUES ('Tenant1'), ('Tenant2');

-- Insert roles
INSERT INTO roles (role_name) VALUES ('Admin'), ('User');

-- Insert users with hashed passwords
-- Replace 'your_password' with actual passwords and use crypt to hash the passwords with a randomly generated salt.
INSERT INTO users (tenant_id, email, hashed_password) VALUES
(1, 'admin@tenant1.com', crypt('password1', gen_salt('bf'))),
(2, 'user@tenant2.com', crypt('password2', gen_salt('bf')));

-- Assuming IDs for roles are 1 for Admin and 2 for User respectively
-- Insert user_roles
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1), -- Admin@Tenant1
(2, 2); -- User@Tenant2

-- Insert products
INSERT INTO products (tenant_id, product_name, box_size) VALUES
(1, 'Product A', 'big'),
(1, 'Product B', 'medium'),
(2, 'Product C', 'small'),
(2, 'Product D', 'big');


