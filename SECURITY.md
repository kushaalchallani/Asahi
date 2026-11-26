# Security Policy

## Supported Versions

Use this table to see which versions of Asahi are currently being supported with security updates.

| Version | Supported |
|---------|-----------|
| latest  | :white_check_mark: |
| minor releases within 1 year | :white_check_mark: |

## Reporting Vulnerabilities

If you believe you have found a security vulnerability in Asahi, please report it responsibly by:

1. **Do not disclose the vulnerability publicly** - This allows the project maintainers to fix the issue before it can be exploited.

2. **Email the security team** at [security@example.com] with the subject line "Asahi Security Vulnerability Report"

3. **Include the following information** in your report:
   - Type of vulnerability (e.g., XSS, SQL injection, authentication bypass, data exposure)
   - Affected components or endpoints
   - Steps to reproduce the issue
   - Potential impact of the vulnerability
   - Any mitigation strategies you've identified

4. **Expected response time**: You can expect an initial response within 5 business days. The maintainers will work with you to understand the issue and develop a fix.

5. **Disclosure timeline**: The project aims to resolve reported vulnerabilities within 30 days. For critical vulnerabilities affecting user data, a fix may be prioritized sooner.

## Security Best Practices

### For Users

- **Keep your password strong and unique** - Use a password that you don't reuse on other sites
- **Be cautious with third-party integrations** - Only connect trusted services to your Asahi account
- **Report suspicious activity** - If you notice unusual account behavior, contact support immediately

### For Contributors

- **Never commit secrets** - API keys, database passwords, and secret tokens should never be committed to the repository
- **Use environment variables** - All sensitive configuration should come from environment variables
- **Follow the code review process** - All changes go through pull request review to catch security issues
- **Run the test suite** - Ensure all tests pass before submitting changes

### Code Security

- **Input validation** - All user inputs should be validated and sanitized
- **SQL injection prevention** - Use parameterized queries (SQLAlchemy ORM handles this)
- **XSS prevention** - Escape user-generated content before rendering in the frontend
- **CSRF protection** - FastAPI's form handling provides CSRF protection
- **Password hashing** - Use the project's established password hashing (pwdlib/argon2)
- **JWT token security** - Keep the secret key secure and rotate regularly
- **HTTPS only** - All production deployments must use HTTPS

## Data Privacy

Asahi is committed to protecting user privacy:

- **Check-in data** - Emotional state and notes are stored securely in PostgreSQL
- **No sensitive third-party data** - Asahi does not integrate with social media or external platforms that require sensitive credentials
- **Data retention** - Users can delete their data at any time through the application
- **Minimal data collection** - Only essential data is collected to provide the mission recommendation feature

## Secure Deployment Checklist

Before deploying Asahi to production:

- [ ] All environment variables are set (DATABASE_URL, ASAHI_SECRET_KEY)
- [ ] CORS is configured for production domains only
- [ ] HTTPS is enabled
- [ ] Database backups are configured
- [ ] Error reporting does not expose stack traces to end users
- [ ] Rate limiting is configured for authentication endpoints
- [ ] Session timeout is configured (30-minute JWT expiry)
- [ ] Dependency versions are up to date
- [ ] No debug mode in production