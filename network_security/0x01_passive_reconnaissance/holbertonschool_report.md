# Passive Reconnaissance Report: holbertonschool.com

## Objective

The objective of this task was to gather as much information as possible about the `holbertonschool.com` domain using Shodan.

The focus of the reconnaissance was:

* Collecting IP addresses and IP ranges related to `holbertonschool.com`
* Identifying technologies and frameworks used across subdomains
* Writing the collected notes in markdown format

## Target Domain

```text
holbertonschool.com
```

## Tool Used

```text
Shodan
```

Shodan was used as a passive reconnaissance tool to identify public information about hosts, services, certificates, HTTP headers, technologies, and infrastructure related to `holbertonschool.com`.

## Shodan Search Queries Used

The following searches were used on the Shodan website:

```text
hostname:holbertonschool.com
ssl.cert.subject.cn:holbertonschool.com
ssl.cert.subject.alt_names:holbertonschool.com
```

## IP Addresses Found

The following IP addresses were visible in the Shodan results for `holbertonschool.com` and its related subdomains:

| IP Address    | Organization / Provider | Notes                                              |
| ------------- | ----------------------- | -------------------------------------------------- |
| 18.188.10.153 | Amazon.com / AWS        | Associated with Holberton School related hostnames |
| 52.14.14.24   | Amazon.com / AWS        | Associated with Holberton School related hostnames |
| 51.15.213.103 | Scaleway / Online SAS   | Shown as a Holberton-related Shodan host result    |

## IP Ranges / Infrastructure Notes

The visible Shodan results show that the domain uses cloud-hosted infrastructure.

| Provider              | Related IPs                | Notes                                                     |
| --------------------- | -------------------------- | --------------------------------------------------------- |
| Amazon.com / AWS      | 18.188.10.153, 52.14.14.24 | Hosts related to `holbertonschool.com` and its subdomains |
| Scaleway / Online SAS | 51.15.213.103              | Additional host result related to the reconnaissance      |

No full CIDR ranges were visible in the screenshot. Therefore, the collected information is limited to the individual IP addresses and their visible hosting providers.

## Subdomains / Hostnames Found

The following hostnames and subdomains were visible in the Shodan results:

```text
holbertonschool.com
www.holbertonschool.com
blog.holbertonschool.com
apply.holbertonschool.com
```

Additional Shodan result titles also showed Holberton-related web portals and forum pages.

## Technologies and Frameworks Found

The following technologies, services, and HTTP security headers were visible in the Shodan results:

| Technology / Header             | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| HTTPS                           | Secure web service exposed on port 443              |
| SSL Certificate                 | SSL/TLS certificate information available in Shodan |
| nginx                           | Web server detected in HTTP response headers        |
| HTTP 200 OK                     | Some hosts returned successful HTTP responses       |
| HTTP 301 / 302 Redirect         | Some hosts redirected to another page or hostname   |
| X-Frame-Options: SAMEORIGIN     | Clickjacking protection header                      |
| X-XSS-Protection: 1; mode=block | Legacy browser XSS protection header                |
| X-Content-Type-Options: nosniff | Prevents MIME type sniffing                         |
| X-Download-Options: noopen      | Browser download protection header                  |

## Technologies by Hostname

| Hostname / Subdomain                                      | IP Address    | Technologies / Observations                           |
| --------------------------------------------------------- | ------------- | ----------------------------------------------------- |
| holbertonschool.com                                       | 18.188.10.153 | HTTPS, SSL certificate, nginx, HTTP redirect          |
| [www.holbertonschool.com](http://www.holbertonschool.com) | 18.188.10.153 | HTTPS, SSL certificate, nginx, HTTP redirect          |
| blog.holbertonschool.com                                  | 52.14.14.24   | HTTPS, SSL certificate, nginx, HTTP 200 OK            |
| apply.holbertonschool.com                                 | 52.14.14.24   | HTTPS, SSL certificate, nginx, HTTP 200 OK            |
| Holberton School web portal                               | 51.15.213.103 | HTTPS, SSL certificate, Holberton-related web service |

## HTTP Headers Observed

The following HTTP headers were visible in the Shodan results:

```text
Server: nginx
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Download-Options: noopen
```

These headers indicate that the web applications use basic browser-side security protections.

## Services Observed

The Shodan results mainly showed web services.

| Port / Service | Notes                                             |
| -------------- | ------------------------------------------------- |
| HTTP           | Web service with redirects and HTTP responses     |
| HTTPS          | TLS-enabled web service with SSL certificate data |

## Passive Reconnaissance Notes

The reconnaissance was performed passively using Shodan.

No exploitation, brute forcing, vulnerability scanning, or active attacks were performed against the target domain.

The collected results show that `holbertonschool.com` uses cloud infrastructure, mainly Amazon Web Services, and exposes web services using HTTPS. The visible HTTP headers indicate the use of nginx and common web security headers.

## Conclusion

Shodan results for `holbertonschool.com` showed multiple related hosts and subdomains, including `www.holbertonschool.com`, `blog.holbertonschool.com`, and `apply.holbertonschool.com`.

The infrastructure appears to use cloud hosting providers such as AWS and Scaleway. The main technologies observed were HTTPS, SSL/TLS certificates, nginx, HTTP redirects, and several HTTP security headers.

The main IP addresses identified were:

```text
18.188.10.153
52.14.14.24
51.15.213.103
```

The main technologies identified were:

```text
HTTPS
SSL/TLS
nginx
HTTP redirects
X-Frame-Options
X-XSS-Protection
X-Content-Type-Options
X-Download-Options
```
