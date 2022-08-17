FROM golang:1.19 AS BUILDER

RUN go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest
RUN xcaddy build --with github.com/gamalan/caddy-tlsredis

FROM debian:11-slim

COPY --from=BUILDER /go/caddy /usr/local/bin/caddy
