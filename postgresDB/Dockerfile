FROM postgres:16.9

RUN mkdir -p /var/lib/postgresql/data

ENV PGDATA=/var/lib/postgresql/data/pgdata

COPY BAckUp.sql .
VOLUME ["/var/lib/postgresql/data"]

EXPOSE 5432

COPY make_backUP.sh /usr/local/bin/make_backUP.sh
RUN chmod +x /usr/local/bin/make_backUP.sh

CMD ["/usr/local/bin/make_backUP.sh"]
