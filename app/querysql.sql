insert into snappies_article (nom,taille,types)  values('Lange','S','C');
insert into snappies_article (nom,taille,types)  values('Lange','M','C');
insert into snappies_article (nom,taille,types)  values('Lange','L','C');

insert into snappies_article (nom,types)  values('Inserts','C');
insert into snappies_article (nom,types)  values('Gants de toilette','U');
insert into snappies_article (nom,types)  values('Sacs poubelles','U');


insert into snappies_caisse (article_id,nbr_articles,test) values (1,40,0);
insert into snappies_caisse (article_id,nbr_articles,test) values (2,40,0);
insert into snappies_caisse (article_id,nbr_articles,test) values (3,40,0);

insert into snappies_caisse (article_id,nbr_articles,test) values (4,0,0);
insert into snappies_caisse (article_id,nbr_articles,test) values (5,0,0);
insert into snappies_caisse (article_id,nbr_articles,test) values (6,0,0);



insert into snappies_tournee(nom,livreur_id ) VALUES ('Tournée Mons',1);
insert into snappies_tournee(nom,livreur_id ) VALUES ('Tournée Charleroi',1);
insert into snappies_tournee(nom,livreur_id ) VALUES ('Tournée Bruxelles',1);

insert into snappies_client(name, numero_telephone, adresse) VALUES ('Rêverie','0485165492','Rue Francisco Ferrer 19 boite 3, 6181 Gouy-Lez-Piéton');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Les ptits loups','0485165492','Rue de la Vielle Place 51, 6001 Marcinelle');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Larbre à cabane','0485165492','Chaussée de Nivelles 212, 6041 gosselies');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Les lutins','0485165492','Rue de Tamines 18, 6224 Wanfercée-Baulet');

insert into snappies_client(name, numero_telephone, adresse) VALUES ('Les Tiffins','0485165492','Rue des Combattants, 59, 1310 La Hulpe');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Cardinal Mercier','0485165492','Rue Souveraine 48, 1050 Bruxelles');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Les Poussins','0485165492','Av. Ducpétiaux 16, 1060 Saint-Gilles');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Saint Joseph','0485165492','Chaussée de Boisfort 40, 1050 Ixelles');


insert into snappies_client(name, numero_telephone, adresse) VALUES ('MMI','0485165492','Dorpsstraat 76, 7850 Edingen');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Royaume','0485165492','Chau. Asse 130, 7850 Enghien');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Gratty','0485165492','Place communale 17, 7830 Silly');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('Boulous','0485165492','Rue de la Coquiane 61, 7850 Petit-Enghien');
insert into snappies_client(name, numero_telephone, adresse) VALUES ('IRSIA','0485165492','Place de Pâturages, 41 7340 Colfontaine');


insert into snappies_user(username, password, is_admin, is_superuser, last_login) VALUES ('billy le livreur','123',false,false,null); --123
insert into snappies_user(username, password, is_admin, is_superuser, last_login) VALUES ('Souli le livreur','123',false,false,null); --123


insert into snappies_user(username, password, is_admin, is_superuser, last_login) VALUES ('souli admin','123',true,true,null); --123
insert into snappies_user(username, password, is_admin, is_superuser, last_login) VALUES ('billy admin','123',true,true,null); --123


-- tournee 1 8
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,1,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,1,1,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,2,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,2,1,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,3,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,3,1,false);


insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,4,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,4,1,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,5,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,5,1,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,6,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,6,1,false);


insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,7,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,7,1,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,8,1,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,8,1,false);

--tournee 2 5


insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,9,2,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,9,2,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,10,2,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,10,2,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,11,2,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,11,2,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,12,2,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,12,2,false);

insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (true,false,13,2,false);
insert into snappies_commande("default", est_modifie, client_id, tournee_id, est_livre) VALUES (false,false,13,2,false);