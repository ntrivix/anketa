/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     4/2/2017 10:14:58 PM                         */
/*==============================================================*/


drop table if exists ANKETA;

drop table if exists CAS;

drop table if exists GRUPA;

drop table if exists IZVESTAJ;

drop table if exists ODGOVOR;

drop table if exists PITANJA_ZA_ANKETU;

drop table if exists PITANJE;

drop table if exists POPUNIO_ANKETU;

drop table if exists PREDAVAC;

drop table if exists PREDMET;

drop table if exists STUDENT;

drop table if exists STUDENT_U_GRUPI;

/*==============================================================*/
/* Table: ANKETA                                                */
/*==============================================================*/
create table ANKETA
(
   ID_ANKETE            int not null auto_increment,
   IME                  varchar(60) not null,
   OTVORENA_OD          datetime not null,
   OTVORENA_DO          datetime not null,
   CREATED_AT           date not null,
   ZA_SVE				boolean default 0,
   primary key (ID_ANKETE)
);

/*==============================================================*/
/* Table: CAS                                                   */
/*==============================================================*/
create table CAS
(
   ID_CAS               int(64) not null auto_increment,
   ID_PREDMET           int not null,
   ID_PREDAVAC          int not null,
   TIP_CASA             char(1) not null default 'P' comment 'Predavanje (P) / Vezbe (V)',
   primary key (ID_CAS)
);

create table GRUPE_NA_CASU
(
   ID_CAS            int not null,
   ID_GRUPA           int not null,
   primary key (ID_CAS, ID_GRUPA)
);

/*==============================================================*/
/* Table: GRUPA                                                 */
/*==============================================================*/
create table GRUPA
(
   ID_GRUPA             int not null auto_increment,
   IME                  varchar(60) not null,
   GODINA               int DEFAULT 1,
   AKTIVNA_OD           datetime not null,
   AKTIVNA_DO           datetime not null,
   primary key (ID_GRUPA)
);

/*==============================================================*/
/* Table: IZVESTAJ                                              */
/*==============================================================*/
create table IZVESTAJ
(
   ID_IZVESTAJ          int not null auto_increment,
   ID_CAS               int not null,
   ID_PITANJA           int not null,
   ID_ANKETE            int,
   PROSEK               float not null,
   KOMENTARI            text,
   CREATED_AT           date not null,
   primary key (ID_IZVESTAJ)
);

/*==============================================================*/
/* Table: ODGOVOR                                               */
/*==============================================================*/
create table ODGOVOR
(
   ID_ODGOVOR           int not null auto_increment,
   ID_PITANJA           int not null,
   ID_CAS               int,
   ID_ANKETE            int not null,
   OCENA                int,
   KOMENTAR             varchar(256),
   primary key (ID_ODGOVOR)
);

/*==============================================================*/
/* Table: PITANJA_ZA_ANKETU                                     */
/*==============================================================*/
create table PITANJA_ZA_ANKETU
(
   ID_ANKETE            int not null,
   ID_PITANJA           int not null,
   primary key (ID_ANKETE, ID_PITANJA)
);

/*==============================================================*/
/* Table: PITANJE                                               */
/*==============================================================*/
create table PITANJE
(
   ID_PITANJA           int not null auto_increment,
   TEKST                varchar(256) not null,
   CREATED_AT           date not null,
   OBAVEZNO				boolean default 1,
   TIP_PITANJA          char(10) not null default 'O' comment 'Opste pitanje (O) / Pitanje o predmetu (P)',
   primary key (ID_PITANJA)
);

/*==============================================================*/
/* Table: POPUNIO_ANKETU                                        */
/*==============================================================*/
create table POPUNIO_ANKETU
(
   ID_STUDENT           int not null,
   ID_ANKETE            int not null,
   primary key (ID_STUDENT, ID_ANKETE)
);

/*==============================================================*/
/* Table: PREDAVAC                                              */
/*==============================================================*/
create table PREDAVAC
(
   ID_PREDAVAC          int not null auto_increment,
   IME                  varchar(60) not null,
   PREZIME              varchar(60) not null,
   MAIL                 varchar(50) not null,
   primary key (ID_PREDAVAC)
);

/*==============================================================*/
/* Table: PREDMET                                               */
/*==============================================================*/
create table PREDMET
(
   ID_PREDMET           int not null auto_increment,
   IME                  varchar(60) not null,
   primary key (ID_PREDMET)
);

/*==============================================================*/
/* Table: STUDENT                                               */
/*==============================================================*/
/*create table STUDENT
(
   ID_STUDENT           int not null auto_increment,
   IME                  varchar(60) not null,
   PREZIME              varchar(60) not null,
   JMBG                 varchar(20) not null,
   INDEKS               varchar(10) not null,
   MAIL                 varchar(50) not null,
   LOZINKA              char(128) not null,
   NADIMAK              varchar(50) not null,
   primary key (ID_STUDENT)
);*/


CREATE TABLE `STUDENT` (
  `ID_STUDENT` int(11) NOT NULL,
  `IME` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PREZIME` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `JMBG` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `INDEKS` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` char(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NADIMAK` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT NULL,
  `remember_token` char(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table STUDENT_NA_CASU
(
   ID_CAS               int not null,
   ID_STUDENT           int not null,
   primary key (ID_CAS, ID_STUDENT)
);

/*==============================================================*/
/* Table: STUDENT_U_GRUPI                                       */
/*==============================================================*/
create table STUDENT_U_GRUPI
(
   ID_GRUPA             int not null,
   ID_STUDENT           int not null,
   primary key (ID_GRUPA, ID_STUDENT)
);

ALTER TABLE `STUDENT`
  ADD PRIMARY KEY (`ID_STUDENT`),
  MODIFY COLUMN ID_STUDENT INT(11) NOT NULL auto_increment,
  ADD UNIQUE KEY `email` (`email`);

alter table CAS add constraint FK_PREDAVAC_NA_CASU foreign key (ID_PREDAVAC)
      references PREDAVAC (ID_PREDAVAC) on delete restrict on update restrict;

alter table CAS add constraint FK_PRIPADAJUCI_PREDMET foreign key (ID_PREDMET)
      references PREDMET (ID_PREDMET) on delete restrict on update restrict;

alter table CAS add constraint FK_PRIPADA_GRUPI foreign key (ID_GRUPA)
      references GRUPA (ID_GRUPA) on delete restrict on update restrict;

alter table IZVESTAJ add constraint FK_RELATIONSHIP_10 foreign key (ID_CAS)
      references CAS (ID_CAS) on delete restrict on update restrict;

alter table IZVESTAJ add constraint FK_RELATIONSHIP_11 foreign key (ID_PITANJA)
      references PITANJE (ID_PITANJA) on delete restrict on update restrict;

alter table IZVESTAJ add constraint FK_RELATIONSHIP_12 foreign key (ID_ANKETE)
      references ANKETA (ID_ANKETE) on delete restrict on update restrict;

alter table ODGOVOR add constraint FK_OCENA_ZA_CAS foreign key (ID_CAS)
      references CAS (ID_CAS) on delete restrict on update restrict;

alter table ODGOVOR add constraint FK_ODGOVOR_NA_PITANJE foreign key (ID_PITANJA)
      references PITANJE (ID_PITANJA) on delete restrict on update restrict;

alter table ODGOVOR add constraint FK_RELATIONSHIP_9 foreign key (ID_ANKETE)
      references ANKETA (ID_ANKETE) on delete restrict on update restrict;

alter table PITANJA_ZA_ANKETU add constraint FK_RELATIONSHIP_13 foreign key (ID_PITANJA)
      references PITANJE (ID_PITANJA) on delete restrict on update restrict;

alter table PITANJA_ZA_ANKETU add constraint FK_RELATIONSHIP_8 foreign key (ID_ANKETE)
      references ANKETA (ID_ANKETE) on delete restrict on update restrict;

alter table POPUNIO_ANKETU add constraint FK_POPUNIO_ANKETU foreign key (ID_STUDENT)
      references STUDENT (ID_STUDENT) on delete restrict on update restrict;

alter table POPUNIO_ANKETU add constraint FK_POPUNIO_ANKETU2 foreign key (ID_ANKETE)
      references ANKETA (ID_ANKETE) on delete restrict on update restrict;

alter table STUDENT_U_GRUPI add constraint FK_STUDENT_U_GRUPI foreign key (ID_GRUPA)
      references GRUPA (ID_GRUPA) on delete restrict on update restrict;

alter table STUDENT_U_GRUPI add constraint FK_STUDENT_U_GRUPI2 foreign key (ID_STUDENT)
      references STUDENT (ID_STUDENT) on delete restrict on update restrict;

alter table STUDENT_NA_CASU add constraint FK_STUDENT_NA_CASU foreign key (ID_CAS)
      references CAS (ID_CAS) on delete restrict on update restrict;

alter table STUDENT_NA_CASU add constraint FK_STUDENT_NA_CASU2 foreign key (ID_STUDENT)
      references STUDENT (ID_STUDENT) on delete restrict on update restrict;

alter table GRUPE_NA_CASU add constraint FK_GRUPE_NA_CASU foreign key (ID_CAS)
      references CAS (ID_CAS) on delete restrict on update restrict;


alter table GRUPE_NA_CASU add constraint FK_GRUPE_NA_CASU2 foreign key (ID_GRUPA)
      references GRUPA (ID_GRUPA) on delete restrict on update restrict;

ALTER TABLE `GRUPA` ADD `GODINA` INT NULL DEFAULT '1' AFTER `AKTIVNA_DO`, ADD INDEX `Godina_studija` (`GODINA`);

      



      

