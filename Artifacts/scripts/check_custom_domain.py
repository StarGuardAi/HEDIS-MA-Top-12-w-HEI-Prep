#!/usr/bin/env python3
"""
Quick DNS + HTTPS connectivity check for custom GitHub Pages domains.

Usage:
    python scripts/check_custom_domain.py influencers.yourdomain.com \
        --url https://influencers.yourdomain.com

The script performs three lightweight validations:
1. DNS resolution (IPv4/IPv6) using socket.getaddrinfo
2. HTTPS handshake to capture certificate subject & issuer
3. HTTP HEAD request to verify status / Location headers

Keeps dependencies to stdlib only so it can run anywhere.
"""

from __future__ import annotations

import argparse
import socket
import ssl
from http.client import HTTPSConnection
from typing import Iterable, Optional, Sequence, Tuple
from urllib.parse import urlparse


def resolve_addresses(hostname: str) -> Sequence[Tuple[str, str]]:
    """Return list of (family, address) tuples for a hostname."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise RuntimeError(f"DNS lookup failed for {hostname}: {exc}") from exc

    results = []
    for family, _, _, _, sockaddr in infos:
        fam_name = "IPv6" if family == socket.AF_INET6 else "IPv4"
        addr = sockaddr[0]
        entry = (fam_name, addr)
        if entry not in results:
            results.append(entry)
    return results


def fetch_certificate(hostname: str, port: int = 443) -> ssl.SSLSocket:
    """Perform TLS handshake and return the SSL socket for inspection."""
    context = ssl.create_default_context()
    raw_sock = socket.create_connection((hostname, port), timeout=10)
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=hostname)
    return ssl_sock


def format_cert_subject(subject: Optional[Iterable]) -> str:
    """Format certificate subject/issuer structure as readable string."""
    if subject is None:
        return "<unknown>"

    subject_parts = []
    if isinstance(subject, dict):
        subject_parts.extend(f"{name}={value}" for name, value in subject.items())
    else:
        for attributes in subject:
            for name, value in attributes:
                subject_parts.append(f"{name}={value}")

    return ", ".join(subject_parts) if subject_parts else "<unknown>"


def check_https_head(url: str, timeout: float = 10.0) -> Tuple[int, dict]:
    """Send an HTTP HEAD request and return status + headers."""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are supported.")

    conn = HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=timeout)
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    conn.request("HEAD", path)
    response = conn.getresponse()
    headers = {k: v for (k, v) in response.getheaders()}
    conn.close()
    return response.status, headers


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DNS + HTTPS checker for custom domains.")
    parser.add_argument("hostname", help="Custom domain hostname (e.g., influencers.example.com)")
    parser.add_argument(
        "--url",
        help="Full HTTPS URL to test (defaults to https://hostname/)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    target_url = args.url or f"https://{args.hostname}/"

    print(f"[DNS] Checking {args.hostname} ...")
    addresses = resolve_addresses(args.hostname)
    for fam, addr in addresses:
        print(f"  - {fam}: {addr}")
    if not addresses:
        print("  ! No addresses resolved.")

    print(f"\n[TLS] Fetching certificate from {args.hostname} ...")
    with fetch_certificate(args.hostname) as ssl_sock:
        cert = ssl_sock.getpeercert()
        issuer = format_cert_subject(cert.get("issuer"))
        subject = format_cert_subject(cert.get("subject"))
        print(f"  - Subject: {subject}")
        print(f"  - Issuer:  {issuer}")
        print(f"  - TLS version: {ssl_sock.version()}")

    print(f"\n[HTTP] Sending HEAD request to {target_url} ...")
    status, headers = check_https_head(target_url)
    print(f"  - Status: {status}")
    location = headers.get("Location")
    if location:
        print(f"  - Location header: {location}")
    cache_control = headers.get("Cache-Control")
    if cache_control:
        print(f"  - Cache-Control: {cache_control}")

    print("\nAll checks completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

