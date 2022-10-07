create schema alt_proc;

create table cmds
(
    cmd_id serial                                      not null
        constraint cmds_pk
            primary key,
    name   varchar                                     not null,
    params json,
    status varchar   default 'WAIT'::character varying not null,
    error  varchar,
    ctime  timestamp default now()                     not null
);

alter table cmds
    owner to alt_proc;

create index cmds_status_index
    on cmds (status);

create table tasks
(
    task_id      serial                                     not null
        constraint tasks_pk
            primary key,
    type         varchar                                    not null,
    name         varchar                                    not null,
    status       varchar default 'PAUSE'::character varying not null,
    project      varchar                                    not null,
    period       integer,
    priority     integer,
    n_fatals     integer,
    n_runs       integer default 1,
    last_proc_id integer
);

alter table tasks
    owner to alt_proc;

create index tasks_status_index
    on tasks (status);

create table events
(
    event_id serial                                      not null
        constraint events_pk
            primary key,
    task_id  integer                                     not null
        constraint events_tasks_fk
            references tasks
            on update cascade on delete cascade,
    title    varchar,
    ctime    timestamp default now()                     not null,
    status   varchar   default 'WAIT'::character varying not null,
    params   json
);

alter table events
    owner to alt_proc;

create index events_status_index
    on events (status);

create table procs
(
    proc_id  serial                                      not null
        constraint procs_pk
            primary key,
    status   varchar   default 'WAIT'::character varying not null,
    result   varchar,
    event_id integer
        constraint procs_events_fk
            references events
            on update cascade on delete cascade,
    ctime    timestamp default now()                     not null,
    stime    timestamp,
    etime    timestamp,
    mtime    timestamp default now()                     not null,
    run_at   timestamp,
    os_pid   integer,
    data     json
);

alter table procs
    owner to alt_proc;

alter table tasks
    add constraint tasks_procs_proc_id_fk
        foreign key (last_proc_id) references procs;

create index procs_status_index
    on procs (status);

create table scripts
(
    script_id serial            not null
        constraint scripts_pk
            primary key,
    proc_id   integer           not null
        constraint scripts_procs_fk
            references procs
            on update cascade on delete cascade,
    script    varchar           not null,
    name      varchar           not null,
    status    varchar           not null,
    result    varchar,
    resources json,
    stime     timestamp,
    etime     timestamp,
    n_runs    integer default 0 not null,
    iscript   integer           not null
);

alter table scripts
    owner to alt_proc;

create table msgs
(
    msg_id    serial                not null
        constraint msgs_pk
            primary key,
    msg       varchar               not null,
    type      varchar               not null,
    active    boolean default true  not null,
    script_id integer               not null
        constraint msgs_scripts_fk
            references scripts
            on update cascade on delete cascade,
    stime     timestamp             not null,
    etime     timestamp             not null,
    n_runs    integer default 1     not null,
    todo      boolean default false not null,
    read      boolean default false not null,
    send      boolean default false not null
);

alter table msgs
    owner to alt_proc;

create table values
(
    key   varchar not null
        constraint values_pk
            primary key,
    value varchar
);

alter table values
    owner to alt_proc;

