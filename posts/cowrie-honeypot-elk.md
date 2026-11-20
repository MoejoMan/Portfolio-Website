---
title: A week of SSH attacks on a public VPS, in numbers
date: 2026-11-19
summary: 34,682 login attempts against one Hetzner box in seven days, 1,128 source IPs, and what nearly half of them were after.
tags: Honeypot, ELK, Cowrie, SSH, Hetzner
draft: true
---

<!--
SCAFFOLD. Numbers are real and verified from your own auth.log.
The prose is yours. Each comment block says what the section needs.
Delete every comment before setting draft: false, they survive into page source.

SOURCE: C:\Users\jhg56\Downloads\auth.log, from ubuntu-4gb-hel1-2,
73,382 lines, 14 to 20 December 2025.

NOT COWRIE. This is the host's own sshd log, from before the honeypot was
rebuilt. Everything below is what real sshd on the public port recorded. Do
not call it honeypot capture. The Cowrie data is a separate, later post.
-->

## Why

<!--
Needed:
- Why the box exists, and why you pulled its auth.log in the first place
  (you downloaded it to test SSHVigil against real data).
- What you expected before you counted. Say it honestly, because the result
  is both more boring and more interesting than most people assume.
-->

## The setup

<!--
Verified from the log, use freely:
- Hetzner 4GB instance in Helsinki, hostname ubuntu-4gb-hel1-2.
- Admin account `echo`. Public key only: zero "Failed password" lines all week.
- All three of your own logins came from 10.66.66.2, inside the WireGuard
  subnet, so real SSH was reachable over the VPN and nothing else.
- On 15 December you locked the cowrie service account and set its shell to
  /usr/sbin/nologin.

Still needed from you: Ubuntu version, and whether fail2ban was running then.
-->

## Seven days of traffic

Between 14 and 20 December 2025 the public SSH port logged **34,682 login
attempts** from **1,128 distinct IP addresses**, against **2,094 distinct
usernames**. A mean of **4,955 a day**. The busiest hour was 08:00 on 14
December with 572. A further 68 attempts arrived with no username at all.

| Day | Attempts |
| --- | --- |
| 2025-12-14 | 6,465 |
| 2025-12-15 | 4,526 |
| 2025-12-16 | 4,770 |
| 2025-12-17 | 6,083 |
| 2025-12-18 | 3,917 |
| 2025-12-19 | 3,913 |
| 2025-12-20 | 5,008 |

## Nearly half of it was one account

| Username | Exists on host | Attempts | Share |
| --- | --- | --- | --- |
| `root` | yes | 15,761 | 45.4% |
| `sol` | no | 1,850 | 5.3% |
| `admin` | no | 1,746 | 5.0% |
| `solv` | no | 1,221 | 3.5% |
| `solana` | no | 1,114 | 3.2% |
| `ubuntu` | no | 880 | 2.5% |
| `user` | no | 705 | 2.0% |
| `test` | no | 394 | 1.1% |
| `postgres` | no | 316 | 0.9% |
| `oracle` | no | 314 | 0.9% |
| `git` | no | 237 | 0.7% |
| `backup` | yes | 192 | 0.6% |

<!--
THE HEADLINE. root took 15,761 attempts, 45.4% of everything, and 945 of the
1,128 attacking IPs tried it. Five out of every six attackers went for root.

So the boring advice is the correct advice, and your own data says so: root
is still the single most attacked account on the internet by a factor of
eight over the next name on the list.

Then the second story, which is the interesting one. The largest non root
cluster is `sol`, `solv`, and `solana`: 4,191 attempts, 12.1% of the total.
Those are Solana validator account names. A meaningful slice of SSH scanning
is not hunting for shells, it is hunting for crypto nodes.

Third thing worth a line: they also walk the default Debian system accounts.
backup (192), daemon (163), www-data (57), then nobody, games, bin, uucp,
mail, and proxy. Those exist on every Debian and Ubuntu install and are
normally nologin, which tells you the scanning is template driven rather
than informed.

And one detail you should definitely include: `echo`, your actual admin
username, was tried exactly once in the whole week.

Also: 780 of the 2,094 usernames were tried exactly once, 37%. Dictionary
spray, not targeting.
-->

### A note on how I counted, and the mistake in my first pass

<!--
KEEP THIS SECTION. It is the most credible thing in the post.

The first version of the analysis counted only lines shaped like
"Invalid user <name> from <ip>". That pattern only ever matches accounts that
do NOT exist on the host. root exists, so root could not appear in the
results at all, and the first pass concluded that nobody attacked root.

Attempts against real accounts log differently:

    Disconnected from authenticating user root <ip> port <n> [preauth]
    Connection reset by authenticating user root <ip> port <n> [preauth]
    Connection closed by authenticating user root <ip> port <n> [preauth]
    error: maximum authentication attempts exceeded for root from <ip>

Counting only one shape understated the total by 15,761 attempts and inverted
the conclusion. Write that up in your own words. Pick the general lesson out
of it: a log parser that matches one message shape silently measures a subset
and reports it as the whole, and you cannot see the gap from inside the
results. Say how you would catch it next time.
-->

## Where it came from

| Source network | Attempts | Share | Distinct hosts |
| --- | --- | --- | --- |
| 80.94.92.0/24 | 2,370 | 6.8% | 10 |
| 45.140.17.0/24 | 2,148 | 6.2% | 2 |
| 91.202.233.0/24 | 2,028 | 5.8% | 1 |
| 45.135.232.0/24 | 1,505 | 4.3% | 1 |
| 92.118.39.0/24 | 857 | 2.5% | 2 |
| 2.57.122.0/24 | 647 | 1.9% | 1 |

<!--
Needed: one evidenced observation. The honest one is that 80.94.92.0/24 sent
6.8% from 10 hosts in a single /24, and 91.202.233.0/24 sent 5.8% from a
single address, so range blocking would have beaten address blocking.

Do NOT assert who owns these ranges or what country they are in unless you
look it up and say how.
-->

## What I changed because of it

<!--
Needed:
- Password auth was already off, which is why there is not one successful
  password login in 34,682 attempts. Was that deliberate?
- Your access is VPN only. Decision or accident?
- Given that root takes 45% of the traffic, what do you actually do about it
  on the next box you build?
- fail2ban: your site claims bans. fail2ban writes to /var/log/fail2ban.log,
  not here, so this log cannot confirm or deny it. If you still have that
  log, pull it and give the real ban count. Otherwise drop the claim.
-->
