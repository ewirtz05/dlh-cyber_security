# Passive Reconnaissance Report: holbertonschool.com

## Objective

The objective of this task was to gather as much passive reconnaissance information as possible about the domain `holbertonschool.com` using Shodan.

The requested information includes:

* IP ranges and IP addresses related to `holbertonschool.com`
* Technologies and frameworks used by subdomains of `holbertonschool.com`
* Notes written as a markdown report

## Target Domain

```text
holbertonschool.com
```

## Tool Used

```text
Shodan CLI
```

Shodan is a search engine for internet-connected systems. It can be used during passive reconnaissance to identify publicly exposed services, open ports, TLS certificate data, hostnames, IP addresses, and detected technologies without directly scanning the target.

## Shodan CLI Status

The Shodan CLI was configured and tested with the following command:

```bash
shodan info
```

The command returned:

```text
Query credits available: 0
Scan credits available: 0
```

This confirms that the Shodan CLI was initialized successfully, but the account had no available query credits.

## Shodan Commands Attempted

The following Shodan commands were used or prepared to gather information about `holbertonschool.com`:

```bash
shodan domain holbertonschool.com
shodan search ssl.cert.subject.cn:holbertonschool.com
shodan search hostname:holbertonschool.com
shodan search org:Holberton
```

## Shodan Results

Each Shodan query returned the following error:

```text
Error: Access denied (403 Forbidden)
```

The reason for this limitation was the account status:

```text
Query credits available: 0
```

Because the Shodan account had no available query credits, Shodan did not return domain, hostname, IP range, service, or technology results.

## IP Ranges and IP Addresses

No confirmed IP ranges or IP addresses could be collected from Shodan because access to Shodan search results was denied.

The following information should be collected once Shodan query credits are available:

* Public IP addresses hosting `holbertonschool.com`
* Public IP addresses linked to subdomains
* Related IP ranges
* ASN information
* Hosting provider or cloud provider information
* Exposed ports and services
* Service banners

## Subdomains to Investigate

The following Holberton-related hostnames and subdomains should be investigated with Shodan once query access is available:

```text
holbertonschool.com
www.holbertonschool.com
blog.holbertonschool.com
apply.holbertonschool.com
intranet.holbertonschool.com
```

Useful Shodan filters for this step include:

```bash
shodan search hostname:holbertonschool.com
shodan search ssl.cert.subject.cn:holbertonschool.com
shodan search ssl.cert.subject.alt_names:holbertonschool.com
```

## Technologies and Frameworks

No confirmed technologies or frameworks could be collected from Shodan because the queries returned `403 Forbidden`.

The following technology categories should be collected from Shodan results when query access is available:

* Web server software
* HTTP and HTTPS services
* TLS certificate information
* CDN or reverse proxy usage
* Cloud hosting provider
* JavaScript frameworks
* CMS or web application framework
* Exposed service banners
* Open ports
* Security headers
* Related hostnames
* SSL/TLS certificate subject and SAN entries

## Passive Reconnaissance Notes

The reconnaissance remained passive. No exploitation, brute forcing, vulnerability scanning, or direct attack was performed.

The main limitation encountered was the Shodan account restriction. Although the Shodan CLI was initialized, the account had zero query credits, which caused Shodan to block all search queries with `403 Forbidden`.

## Conclusion

The Shodan CLI was correctly configured, but the account did not have query credits available. As a result, Shodan search queries for `holbertonschool.com` could not return IP ranges, related hosts, detected technologies, or service information.

Once Shodan query credits are available, the prepared commands can be rerun to collect real results for:

* IP ranges and IP addresses
* Subdomains
* Open ports
* Detected technologies
* TLS certificate data
* Hosting and ASN information
* Service banners
