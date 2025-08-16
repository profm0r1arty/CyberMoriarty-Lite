# CyberMoriarty Lite

## Overview

CyberMoriarty Lite is a mobile-friendly web security pentesting tool designed for Filipino cybersecurity practitioners. The application provides basic security scanning capabilities through a Taglish (Filipino-English) conversational interface, making cybersecurity tools more accessible to local users. Built with Kivy for cross-platform mobile deployment, it performs website reconnaissance, security header analysis, administrative interface discovery, and basic XSS testing.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **UI Framework**: Kivy-based mobile application with declarative KV language layouts
- **Design Pattern**: Single-screen interface with scrollable results display
- **Mobile Optimization**: Touch-friendly controls with appropriate spacing (dp units) and responsive design
- **User Experience**: Bilingual Taglish interface to serve Filipino cybersecurity community

### Backend Architecture
- **Core Engine**: Modular Python architecture with separate reconnaissance and scanning components
- **Intent Recognition**: Rule-based natural language processing using regex patterns for Taglish commands
- **Security Modules**:
  - Reconnaissance engine for DNS resolution and HTTP fingerprinting
  - Security header validation against industry standards
  - Administrative interface discovery using common path enumeration
  - Basic XSS reflection testing capabilities

### Assistant System
- **Language Processing**: Pattern-matching intent detection supporting Filipino and English commands
- **Result Interpretation**: Context-aware explanation engine that translates technical findings into user-friendly Taglish
- **Conversational Flow**: Simple command-response interaction model suitable for mobile usage

### Security Scanning Framework
- **Header Analysis**: Validates presence of critical security headers (CSP, X-Frame-Options, HSTS, etc.)
- **Surface Discovery**: Enumerates common administrative endpoints using predefined path lists
- **Vulnerability Testing**: Performs basic reflection-based XSS detection
- **Risk Assessment**: Categorizes findings with security recommendations in accessible language

## External Dependencies

### Core Libraries
- **Kivy**: Cross-platform Python framework for mobile app development and UI rendering
- **Requests**: HTTP library for web reconnaissance and security testing operations
- **Socket**: Built-in Python networking library for DNS resolution and network operations

### Development Tools
- **Buildozer**: Android APK packaging and deployment system for Python applications
- **Threading**: Asynchronous operation handling to maintain responsive UI during scans

### Network Dependencies
- **DNS Services**: System DNS resolution for target identification and IP mapping
- **HTTP/HTTPS Protocols**: Web service communication for reconnaissance and vulnerability testing
- **TLS/SSL**: Secure connection validation and encryption status detection
