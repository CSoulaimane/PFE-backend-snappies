insert into snappies_article (id_article, nom,taille,types)  values(1,'Lange','S','C');
insert into snappies_article (id_article,nom,taille,types)  values(2,'Lange','M','C');
insert into snappies_article (id_article ,nom,taille,types)  values(3,'Lange','L','C');

insert into snappies_article (id_article,nom,types)  values(4,'Inserts','C');
insert into snappies_article (id_article,nom,types)  values(5,'Gants de toilette','U');
insert into snappies_article (id_article, nom,types)  values(6,'Sacs poubelles','U');


insert into snappies_caisse (id_caisse,article_id,nbr_articles,test) values (1,1,40,0);
insert into snappies_caisse (id_caisse,article_id,nbr_articles,test) values (2,2,40,0);
insert into snappies_caisse (id_caisse, article_id,nbr_articles,test) values (3,3,40,0);

insert into snappies_caisse (id_caisse,article_id,nbr_articles,test) values (4,4,0,0);
insert into snappies_caisse (id_caisse,article_id,nbr_articles,test) values (5,5,0,0);
insert into snappies_caisse (id_caisse,article_id,nbr_articles,test) values (6,6,0,0);


insert into snappies_user(id_user,username, password, is_admin, is_superuser, last_login) VALUES (150,'billy_livreur','pbkdf2_sha256$600000$TCYAPvCx7Ofu9R2PbDYSJ5$hUlO3LxYU2h8A6tYsU32CSySOXTcvBooIAFNsZnxM8c=',false,false,null); --123
insert into snappies_user(id_user,username, password, is_admin, is_superuser, last_login) VALUES (151,'souli_livreur','pbkdf2_sha256$600000$TCYAPvCx7Ofu9R2PbDYSJ5$hUlO3LxYU2h8A6tYsU32CSySOXTcvBooIAFNsZnxM8c=',false,false,null); --123


insert into snappies_user(id_user,username, password, is_admin, is_superuser, last_login) VALUES (152,'souli_admin','pbkdf2_sha256$600000$TCYAPvCx7Ofu9R2PbDYSJ5$hUlO3LxYU2h8A6tYsU32CSySOXTcvBooIAFNsZnxM8c=',true,true,null); --123
insert into snappies_user(id_user, username, password, is_admin, is_superuser, last_login) VALUES (153,'billy_admin','pbkdf2_sha256$600000$TCYAPvCx7Ofu9R2PbDYSJ5$hUlO3LxYU2h8A6tYsU32CSySOXTcvBooIAFNsZnxM8c=',true,true,null); --123


insert into snappies_tournee(id_tournee,nom,livreur_id ) VALUES (1,'Tournée Mons',150);
insert into snappies_tournee(id_tournee,nom,livreur_id ) VALUES (2,'Tournée Charleroi',151);
insert into snappies_tournee(id_tournee,nom,livreur_id ) VALUES (3,'Tournée Bruxelles',151);

insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (1,'Rêverie','0485165492','Rue Francisco Ferrer 19 boite 3, 6181 Gouy-Lez-Piéton');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (2,'Les ptits loups','0485165492','Rue de la Vielle Place 51, 6001 Marcinelle');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (3,'Larbre à cabane','0485165492','Chaussée de Nivelles 212, 6041 gosselies');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (4,'Les lutins','0485165492','Rue de Tamines 18, 6224 Wanfercée-Baulet');

insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (5,'Les Tiffins','0485165492','Rue des Combattants, 59, 1310 La Hulpe');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (6,'Cardinal Mercier','0485165492','Rue Souveraine 48, 1050 Bruxelles');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (7,'Les Poussins','0485165492','Av. Ducpétiaux 16, 1060 Saint-Gilles');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (8,'Saint Joseph','0485165492','Chaussée de Boisfort 40, 1050 Ixelles');


insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (9,'MMI','0485165492','Dorpsstraat 76, 7850 Edingen');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (10,'Royaume','0485165492','Chau. Asse 130, 7850 Enghien');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (11,'Gratty','0485165492','Place communale 17, 7830 Silly');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (12,'Boulous','0485165492','Rue de la Coquiane 61, 7850 Petit-Enghien');
insert into snappies_client(id_client,name, numero_telephone, adresse) VALUES (13,'IRSIA','0485165492','Place de Pâturages, 41 7340 Colfontaine');




-- tournee 1 8

-- c 1 2
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (1,true,false,1,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (2,false,false,1,1,false);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,1);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,2);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,1);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,2);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,5,5,1);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,5,5,2);


-- c 3 4

insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (3,true,false,2,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (4,false,false,2,1,false);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,3);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,4);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,3);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,4);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,3);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,4);

-- c 5 6
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (5,true,false,3,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (6,false,false,3,1,false);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,5);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,6);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,5);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,6);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,5);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,6);

-- c 7 8

insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (7,true,false,4,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (8,false,false,4,1,false);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,7);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,8);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,7);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,8);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,7);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,8);
-- c 9 10

insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (9,true,false,5,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (10,false,false,5,1,false);


insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,9);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,10);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,9);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,10);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,9);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,10);
-- c 11 12

insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (11,true,false,6,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (12,false,false,6,1,false);


insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,11);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,12);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,11);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,12);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,11);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,12);
-- c 13 14

insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (13,true,false,7,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (14,false,false,7,1,false);


insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,13);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,14);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,13);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,14);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,13);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,14);
-- c 15 16

insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (15,true,false,8,1,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (16,false,false,8,1,false);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,15);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,16);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,15);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,16);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,15);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,16);



--tournee 2 5

-- 17 18
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (17,true,false,9,2,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (18,false,false,9,2,false);


insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,17);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,18);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,17);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,18);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,17);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,18);

-- 19 20
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (19,true,false,10,2,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (20,false,false,10,2,false);


insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,19);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,20);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,19);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,20);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,19);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,20);

--21 22
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (21,true,false,11,2,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (22,false,false,11,2,false);


insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,21);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,22);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,21);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,22);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,21);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,22);

--23 24
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (23,true,false,12,2,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (24,false,false,12,2,false);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,23);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,24);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,23);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,24);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,23);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,24);

--25 26
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (25,true,false,13,2,false);
insert into snappies_commande(id_commande,"default", est_modifie, client_id, tournee_id, est_livre) VALUES (26,false,false,13,2,false);


insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,25);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (3,0,1,26);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,25);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (5,0,2,26);

insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,25);
insert into snappies_caisse_commande(nbr_caisses, unite, caisse_id, commande_id) VALUES (0,10,6,26);




