FROM golang:1.21 AS BUILDER

RUN go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest
RUN xcaddy build --with github.com/techknowlogick/certmagic-s3 --with github.com/caddy-dns/cloudflare

FROM debian:11-slim

RUN apt update && apt install -y ca-certificates
COPY --from=BUILDER /go/caddy /usr/local/bin/caddy
