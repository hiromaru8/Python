



CREATE TABLE combination_unit (
    src_id      INTEGER,
    dest_id     INTEGER,
    data1       blob,
    data2       blob,
    PRIMARY KEY (src_id, dest_id);
)
CREATE TABLE single_unit (
    id      INTEGER,
    data1       blob,
    data2       blob,
    PRIMARY KEY (id);
)
