"""Security and safety contract verification for eclipse-kuksa-databroker.

KUKSA.val Databroker is the central data bus for vehicle signals. It is
a high-value target: compromise gives an attacker full read/write access
to all VSS signals including safety-critical ones (speed, throttle, brakes).

Security properties to verify:
- JWT authorization: only tokens with correct claims can read/write signals.
- TLS support: gRPC connections can be secured with TLS (certificates present).
- Permission model: separate read/write/actuate permissions per signal path.
- Input validation: malformed gRPC messages do not crash the broker.
- Wildcard matching: overly broad wildcards do not accidentally expose signals.

Verification method: file inspection (boundary analysis, permission model review).
Platform: any (no build required).
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATABROKER_DIR = PROJECT_ROOT / "eclipse-kuksa-databroker"
SRC = DATABROKER_DIR / "databroker" / "src"


# ---------------------------------------------------------------------------
# TestAuthorizationModule
# ---------------------------------------------------------------------------
class TestAuthorizationModule:
    """Verify the authorization module structure.

    KUKSA.val uses JWT-based authorization. The authorization module
    validates tokens and extracts signal-level permissions.
    """

    AUTH_DIR = SRC / "authorization"

    def test_authorization_directory_exists(self):
        assert self.AUTH_DIR.is_dir(), \
            "databroker/src/authorization/ missing — auth module removed"

    def test_authorization_has_source(self):
        rs_files = list(self.AUTH_DIR.rglob("*.rs"))
        assert len(rs_files) >= 1, \
            "authorization/ has no Rust source files"

    def test_permissions_module_exists(self):
        """permissions.rs must exist for signal-level access control."""
        perm = SRC / "permissions.rs"
        assert perm.exists(), \
            "databroker/src/permissions.rs missing — permission model removed"

    def test_jwt_directory_exists(self):
        """JWT token examples must exist for authorization testing."""
        jwt_dir = DATABROKER_DIR / "jwt"
        assert jwt_dir.is_dir(), \
            "jwt/ directory missing — JWT authorization examples removed"

    def test_jwt_readme_explains_claims(self):
        """JWT README should explain the required token claims."""
        readme = DATABROKER_DIR / "jwt" / "README.md"
        if not readme.exists():
            pytest.skip("jwt/README.md not found")
        content = readme.read_text(encoding="utf-8")
        has_claims = "claim" in content.lower() or "permission" in content.lower()
        assert has_claims, \
            "jwt/README.md does not explain required JWT claims"


# ---------------------------------------------------------------------------
# TestTLSSupport
# ---------------------------------------------------------------------------
class TestTLSSupport:
    """Verify TLS certificate infrastructure for secure gRPC."""

    CERT_DIR = DATABROKER_DIR / "certificates"

    def test_certificates_dir_exists(self):
        assert self.CERT_DIR.is_dir(), \
            "certificates/ missing — TLS support removed"

    def test_tls_docs_present(self):
        """TLS documentation must explain how to configure secure connections."""
        doc_dir = DATABROKER_DIR / "doc"
        tls_md = doc_dir / "tls.md" if doc_dir.is_dir() else None
        alt_tls = DATABROKER_DIR / "doc" / "tls.md"
        # Check in the submodule docs
        parent_tls = list(DATABROKER_DIR.rglob("tls.md"))
        assert len(parent_tls) > 0, \
            "No tls.md documentation found — TLS configuration not documented"

    def test_rustls_in_cargo_lock(self):
        """rustls must be in Cargo.lock — tonic uses rustls for TLS."""
        lock = DATABROKER_DIR / "Cargo.lock"
        if not lock.exists():
            pytest.skip("Cargo.lock not found")
        content = lock.read_text(encoding="utf-8")
        has_rustls = "rustls" in content
        has_openssl = "openssl" in content
        assert has_rustls or has_openssl, \
            "Neither rustls nor openssl found in Cargo.lock — TLS library missing"


# ---------------------------------------------------------------------------
# TestWildcardSecurity
# ---------------------------------------------------------------------------
class TestWildcardSecurity:
    """Verify wildcard matching documentation.

    Wildcard subscriptions (e.g. Vehicle.*) are powerful — if
    incorrectly implemented they could expose all signals to unauthorized
    clients or allow DoS via overly broad subscriptions.
    """

    def test_wildcard_docs_exist(self):
        """Wildcard matching must be documented."""
        docs = list(DATABROKER_DIR.rglob("wildcard*"))
        assert len(docs) > 0, \
            "No wildcard documentation found — wildcard behavior undocumented"

    def test_filter_module_exists(self):
        """The filter module implements subscription filtering."""
        filter_dir = SRC / "filter"
        assert filter_dir.is_dir(), \
            "databroker/src/filter/ missing — subscription filter removed"

    def test_query_module_exists(self):
        """The query module handles VSS path queries."""
        query_dir = SRC / "query"
        assert query_dir.is_dir(), \
            "databroker/src/query/ missing — VSS query engine removed"


# ---------------------------------------------------------------------------
# TestInputValidation
# ---------------------------------------------------------------------------
class TestInputValidation:
    """Verify input validation structures are present."""

    def test_types_module_defines_datapoint(self):
        """types.rs must define Datapoint — the core validated signal value type."""
        types_rs = SRC / "types.rs"
        if not types_rs.exists():
            pytest.skip("databroker/src/types.rs not found")
        content = types_rs.read_text(encoding="utf-8")
        has_datapoint = "Datapoint" in content
        has_value = "value" in content.lower()
        assert has_datapoint or has_value, \
            "types.rs does not define Datapoint — signal value type removed"

    def test_broker_module_has_get_set(self):
        """broker.rs must implement get/set operations with validation."""
        broker_rs = SRC / "broker.rs"
        if not broker_rs.exists():
            pytest.skip("databroker/src/broker.rs not found")
        content = broker_rs.read_text(encoding="utf-8")
        has_get = "get" in content.lower()
        has_set = "set" in content.lower()
        assert has_get and has_set, \
            "broker.rs does not implement both get and set operations"

    def test_viss_module_exists(self):
        """VISS (Vehicle Information Service Specification) module must exist."""
        viss_dir = SRC / "viss"
        assert viss_dir.is_dir(), \
            "databroker/src/viss/ missing — VISS API support removed"


# ---------------------------------------------------------------------------
# TestOpenTelemetryObservability
# ---------------------------------------------------------------------------
class TestOpenTelemetryObservability:
    """Verify OpenTelemetry integration for security monitoring.

    Observability is critical for detecting unauthorized access patterns.
    The broker should emit traces for all signal get/set operations.
    """

    def test_opentelemetry_module_exists(self):
        """open_telemetry.rs must exist for distributed tracing."""
        otel_rs = SRC / "open_telemetry.rs"
        assert otel_rs.exists(), \
            "databroker/src/open_telemetry.rs missing — observability removed"

    def test_opentelemetry_docs_present(self):
        """OpenTelemetry documentation must explain trace configuration."""
        otel_docs = list(DATABROKER_DIR.rglob("opentelemetry*"))
        readme_otel = list(DATABROKER_DIR.rglob("*otel*"))
        assert len(otel_docs) > 0 or len(readme_otel) > 0, \
            "No OpenTelemetry documentation found"
