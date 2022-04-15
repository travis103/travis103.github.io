 FROM golang:alpine3.10 as builder

RUN apk add --no-cache \
            git
RUN go get -insecure -u v2ray.com/core/... && \
    go build -o $GOPATH/bin/v2ray v2ray.com/core/main && \
    go build -o $GOPATH/bin/v2ctl v2ray.com/core/infra/control/main

FROM alpine:latest

LABEL maintainer "Darian Raymond <admin@v2ray.com>"

RUN mkdir /usr/bin/v2ray
COPY --from=builder /go/bin/v2ray /usr/bin/v2ray/
COPY --from=builder /go/bin/v2ctl /usr/bin/v2ray/
COPY --from=builder /go/src/v2ray.com/core/release/config/geoip.dat /usr/bin/v2ray/
COPY --from=builder /go/src/v2ray.com/core/release/config/geosite.dat /usr/bin/v2ray/

RUN set -ex && \
    chmod +x /usr/bin/v2ray/v2ray && \
    chmod +x /usr/bin/v2ray/v2ctl

ENV PATH /usr/bin/v2ray:$PATH

CMD ["v2ray", "-config=/etc/v2ray/config.json"]
