---
title: A week of SSH attacks on a public VPS, in numbers
date: 2026-11-19
summary: 18,482 login attempts against one Hetzner box in seven days, 2,083 usernames, and the one finding I did not expect.
tags: Honeypot, ELK, Cowrie, SSH, Hetzner
draft: true
---

<!--
SCAFFOLD. The numbers below are real and verified from your own auth.log.
The prose is yours to write. Each comment block says what the section needs.
Delete every comment before setting draft: false, they survive into page source.

SOURCE OF THE DATA: C:\Users\jhg56\Downloads\auth.log, taken from
ubuntu-4gb-hel1-2, 73,382 lines, 14 to 20 December 2025.

IMPORTANT AND NOT OPTIONAL: this is the host's own sshd log. It is NOT
Cowrie's log. Everything in the data section below is what real sshd on the
public port recorded. Do not describe it as honeypot capture, because it is
not, and the difference is exactly the kind of thing an interviewer will
pick at. If you want Cowrie's own numbers, the JSON log is still on the box
and we pull it separately.
-->

## Why

<!--
Needed:
- Why the box exists at all. It runs your WireGuard VPN and the Cowrie
  honeypot, so say which came first and what you were trying to learn.
- What you expected the attack traffic to look like before you read the log.
  Most people expect root and password guessing. You got neither, which is
  the whole point of the post, so set that expectation up here.
-->

## The setup

<!--
Verified from the log itself, use these freely:
- Host is a Hetzner 4GB instance in Helsinki, hostname ubuntu-4gb-hel1-2.
- Your admin account is `echo`.
- Public key authentication only. Across the whole week there are zero
  "Failed password" lines, which means password auth was already disabled.
- All three of your own logins in that week came from 10.66.66.2, which is
  inside the WireGuard subnet. Your real SSH is reachable over the VPN and
  nothing else.
- On 15 December you locked the cowrie service account and set its shell to
  /usr/sbin/nologin (usermod -L cowrie, usermod -s /usr/sbin/nologin cowrie).

Still needed from you:
- Ubuntu version, Cowrie version, ELK versions.
- Which port Cowrie listens on and how traffic reaches it.
- How Cowrie's JSON log gets into Elasticsearch.
- Whether fail2ban is actually running, since you list it as a skill.
-->

```bash
Paste the real config here. The iptables rule, the sshd_config lines that
turn off password auth, and the Filebeat or Logstash pipeline.
```

## Seven days of traffic

Between 14 and 20 December 2025 the public SSH port logged **18,482 invalid user
attempts** from **1,033 distinct IP addresses**, trying **2,083 distinct
usernames**. That is a mean of **2,640 a day**. The busiest single hour was
22:00 on 17 December, with 292 attempts.

A further 68 attempts arrived with an empty username, giving 18,550 in total.

| Day | Attempts |
| --- | --- |
| 2025-12-14 | 3,554 |
| 2025-12-15 | 2,407 |
| 2025-12-16 | 2,529 |
| 2025-12-17 | 3,011 |
| 2025-12-18 | 1,969 |
| 2025-12-19 | 2,166 |
| 2025-12-20 | 2,846 |

<!--
Needed: one line on whether the dip on 18 December means anything, or whether
this is just how steady the background noise is. Do not over read it.
-->

### What they tried to log in as

| Username | Attempts | Share |
| --- | --- | --- |
| `sol` | 1,850 | 10.0% |
| `admin` | 1,746 | 9.4% |
| `solv` | 1,221 | 6.6% |
| `solana` | 1,114 | 6.0% |
| `ubuntu` | 880 | 4.8% |
| `user` | 705 | 3.8% |
| `test` | 394 | 2.1% |
| `postgres` | 316 | 1.7% |
| `oracle` | 314 | 1.7% |
| `git` | 237 | 1.3% |

<!--
This is your headline finding and you should lead the post with it.

`root` was tried ZERO times as an invalid user. It appears 13 times in the
whole week, and only as "maximum authentication attempts exceeded for root",
from five IPs. Nobody is brute forcing root any more.

Instead, three of the top four usernames are Solana validator accounts.
Usernames beginning "sol" account for 4,191 attempts, 22.7% of everything.
These bots are not hunting for a shell, they are hunting for crypto nodes.

Write this up in your own words. The point to make: the threat model people
teach (root, password guessing) is not the threat model the internet is
actually running. Say what that implies for how you would harden a box.

Also worth a line: 778 of the 2,083 usernames were tried exactly once, 37%.
That is dictionary spray, not targeting.
-->

### Where it came from

| Source network | Attempts | Share | Distinct hosts |
| --- | --- | --- | --- |
| 80.94.92.0/24 | 2,367 | 12.8% | 10 |
| 45.135.232.0/24 | 884 | 4.8% | 1 |
| 92.118.39.0/24 | 851 | 4.6% | 2 |
| 2.57.122.0/24 | 647 | 3.5% | 1 |
| 195.178.110.0/24 | 605 | 3.3% | 1 |
| 45.148.10.0/24 | 459 | 2.5% | 2 |
| 94.156.152.0/24 | 297 | 1.6% | 1 |
| 45.78.219.0/24 | 250 | 1.4% | 24 |

<!--
Needed: one observation you can evidence. The honest one is that 80.94.92.0/24
alone accounts for 12.8% of all attempts across 10 different hosts in the
same /24, so a single network is responsible for an eighth of the traffic and
blocking the range would be more effective than blocking IPs one at a time.
Contrast it with 45.78.219.0/24, which sent fewer attempts from 24 hosts.

Do NOT assert who owns these ranges or what country they are in unless you
actually look it up and say how you looked it up.
-->

## What I changed because of it

<!--
Needed, and this is the section that makes the post worth reading:
- Password auth was already off. Say whether that was deliberate.
- Your own access is VPN only. Was that a decision or an accident?
- Given that root is not the target and service accounts are, what would you
  do differently on the next box you build?
- Did you add any fail2ban or firewall rules after reading this?
-->

## Running a honeypot without making things worse

<!--
Needed:
- Cowrie's fake shell gives no real network access, but say what you checked.
- You locked the cowrie account and gave it nologin. Say why that matters,
  since it is a real precaution you took and it is in the log.
- The honeypot shares a box with your WireGuard VPN. Address that directly.
  A reader will spot it and it is the first thing I would ask you about.
- Hetzner's acceptable use position, if you checked it.
-->
