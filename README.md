# Software Requirements Specification (SRS)

## Table of Contents
1. [Introduction](#introduction)
   1.1 [Purpose](#purpose)
   1.2 [Scope](#scope)
   1.3 [Definitions, Acronyms, and Abbreviations](#definitions-acronyms-and-abbreviations)
   1.4 [References](#references)
   1.5 [Overview](#overview)
2. [Overall Description](#overall-description)
   2.1 [Product Perspective](#product-perspective)
   2.2 [Product Functions](#product-functions)
   2.3 [User Characteristics](#user-characteristics)
   2.4 [Constraints](#constraints)
   2.5 [Assumptions and Dependencies](#assumptions-and-dependencies)
3. [Specific Requirements](#specific-requirements)
   3.1 [Functional Requirements](#functional-requirements)
   3.2 [Non-Functional Requirements](#non-functional-requirements)
   3.3 [External Interface Requirements](#external-interface-requirements)
4. [System Features](#system-features)
   4.1 [Frontend](#frontend)
   4.2 [Backend](#backend)
   4.3 [AWS Integration](#aws-integration)
   4.4 [Deep Learning Components](#deep-learning-components)
5. [Business Modeling and Monetization](#business-modeling-and-monetization)
6. [Appendix](#appendix)
   6.1 [Feedback and Improvements](#feedback-and-improvements)

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to outline the Software Requirements Specification (SRS) for the AdVenture project, which aims to provide users with an AI-powered platform to generate advertisements. This document serves as a guide for the development and deployment of the system.

### 1.2 Scope
The AdVenture project involves developing a web application that allows users to create advertisements by uploading product images and providing text prompts. The system will generate backgrounds, product image variations, and suggest ad text using advanced machine learning models. The backend will be hosted on AWS EC2, and the frontend will be hosted on AWS Amplify.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS**: Software Requirements Specification
- **AWS**: Amazon Web Services
- **EC2**: Elastic Compute Cloud
- **DRF**: Django Rest Framework
- **GAN**: Generative Adversarial Network
- **StackGAN**: Stacked Generative Adversarial Network
- **UI/UX**: User Interface/User Experience
- **SVG**: Scalable Vector Graphics
- **API**: Application Programming Interface
- **CI/CD**: Continuous Integration/Continuous Deployment

### 1.4 References
- AWS Documentation: [https://aws.amazon.com/documentation/](https://aws.amazon.com/documentation/)
- Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- React Konva Documentation: [https://konvajs.org/docs/react/](https://konvajs.org/docs/react/)
- TensorFlow Documentation: [https://www.tensorflow.org/](https://www.tensorflow.org/)

### 1.5 Overview
This SRS document details the system's overall description, specific requirements, system features, business modeling, and monetization strategies, along with feedback and improvements based on stakeholder inputs.

## 2. Overall Description

### 2.1 Product Perspective
The AdVenture project is designed as a web-based application that integrates machine learning models for ad generation. It aims to provide a user-friendly interface for creating professional advertisements.

### 2.2 Product Functions
- User uploads a product image (optional) and provides a text prompt for the ad.
- System generates a background image based on the prompt.
- System generates variations of the product image.
- System suggests ad text using language models.
- Users can interact with the ad elements on a canvas, similar to Photoshop layers.
- Users can download the final ad in various formats (JPG, PNG, SVG).

### 2.3 User Characteristics
- **Guest Users**: Can generate ads but need to watch ads to see results and save high-quality images.
- **Registered Users**: Have access to additional features and can save high-quality images without watching ads.

### 2.4 Constraints
- The system must be responsive and handle multiple deep learning tasks efficiently.
- Must adhere to AWS usage policies and limitations.
- Ensure security and privacy of user data.

### 2.5 Assumptions and Dependencies
- Users have access to the internet and modern web browsers.
- Dependence on AWS services for hosting and machine learning model deployment.

## 3. Specific Requirements

### 3.1 Functional Requirements
- **User Authentication**: Users can register, log in, and manage their accounts.
- **Ad Creation**:
  - Upload product images.
  - Input text prompts.
  - Generate and edit ad components (background, product variations, text).
- **Machine Learning Integration**:
  - Deploy models using AWS SageMaker and Lambda.
  - Real-time ad generation and editing.
- **Canvas Interaction**:
  - Layer-based editing (background, product image, text).
  - Save and download final ads.

### 3.2 Non-Functional Requirements
- **Performance**: Ensure quick response times for model predictions.
- **Scalability**: Handle increasing loads with efficient resource management.
- **Security**: Protect user data with encryption and secure authentication.
- **Usability**: Provide a user-friendly interface for ad creation and editing.

### 3.3 External Interface Requirements
- **Frontend**: Developed using Next.js and React Konva for interactive canvas.
- **Backend**: Developed using Django and DRF for API management.
- **AWS Integration**: Utilize SageMaker for model deployment and Lambda for text generation.

## 4. System Features

### 4.1 Frontend
- **Next.js**: For server-side rendering and improved SEO.
- **React Konva**: For creating an interactive canvas to manipulate ad elements.
- **Features**:
  - Upload product images.
  - Input text prompts.
  - Interactive canvas for editing ad components.
  - Save and download options.

### 4.2 Backend
- **Django**: For building the backend server.
- **Django Rest Framework (DRF)**: For creating RESTful APIs.
- **Django Channels**: For handling real-time updates and interactions on the canvas.
- **Features**:
  - User authentication and management.
  - API endpoints for ad generation and editing.
  - Real-time updates for canvas interactions.

### 4.3 AWS Integration
- **AWS EC2**: Hosting the main backend server.
- **AWS Amplify**: Hosting the frontend application.
- **AWS SageMaker**: Deploying StackGAN models for background and product image generation.
- **AWS Lambda**: Deploying transformer models for text generation.
- **Features**:
  - Model deployment and management.
  - Real-time inference and prediction services.
  - Integration with Django backend for seamless operation.

### 4.4 Deep Learning Components
- **StackGAN**: For generating high-quality background images and product image variations.
- **Heatmaps and Saliency Maps**: For optimizing text placement on the ad.
- **Transformer Models**: For generating suggestive ad text.
- **Features**:
  - Training on large datasets using Google Colab or AWS.
  - Deploying optimized models for efficient inference.
  - Combining model outputs to generate comprehensive ads.

## 5. Business Modeling and Monetization
- **Guest Users**: View ads before seeing results and saving high-quality images.
- **Registered Users**: Subscription plans for ad-free experience and additional features.
- **Ad-Supported Model**: Revenue generation through displayed ads.
- **Business Model**:
  - Initial free access with basic features.
  - Premium features and high-quality image downloads available through subscriptions.

## 6. Appendix

### 6.1 Feedback and Improvements
Based on feedback from teachers and stakeholders:
1. **Model Deployment**:
   - Deploy the backend on AWS EC2, use AWS SageMaker for StackGAN, and AWS Lambda for transformer models.
2. **Ad Components**:
   - Include additional graphics such as shapes, icons, logos, and branding.
   - Ensure product images are transparent PNGs.
   - Add advanced features like 3D elements, background overlays, and special patterns.
3. **Business Model**:
   - Implement a freemium model similar to the Remini app, with ads for free users and premium options for high-quality downloads.

This SRS document outlines the comprehensive requirements and design for the AdVenture project, ensuring a clear roadmap for development and deployment.
