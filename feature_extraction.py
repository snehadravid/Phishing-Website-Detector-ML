from urllib.parse import urlparse
import ipaddress


def has_ip_address(url):
    try:
        hostname = urlparse(url).hostname

        if hostname:
            ipaddress.ip_address(hostname)
            return 1

    except ValueError:
        pass

    return 0


def extract_features(url):
    parsed = urlparse(url)

    hostname = parsed.hostname if parsed.hostname else ""

    features = {
        "URLLength": len(url),
        "DomainLength": len(hostname),
        "IsDomainIP": has_ip_address(url),
        "NoOfSubDomain": max(0, hostname.count(".") - 1),
        "NoOfEqualsInURL": url.count("="),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
        "IsHTTPS": int(parsed.scheme.lower() == "https"),
        "NoOfLettersInURL": sum(character.isalpha() for character in url),
        "NoOfDegitsInURL": sum(character.isdigit() for character in url),
        "NoOfOtherSpecialCharsInURL": sum(
            not character.isalnum() and character not in "/.-_:"
            for character in url
        ),
    }

    return features