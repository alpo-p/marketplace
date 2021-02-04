INSERT INTO categories (name) VALUES ('Autot');
INSERT INTO categories (name) VALUES ('Puhelimet');
INSERT INTO categories (name) VALUES ('Vuokra-asunnot');
INSERT INTO categories (name) VALUES ('Tietokoneet');
INSERT INTO categories (name) VALUES ('Muu elektroniikka');

INSERT INTO items (category_id, name, date_added, visible) VALUES (1, 'Tesla', NOW(), TRUE);
INSERT INTO items (category_id, name, date_added, visible) VALUES (1,'Golf', NOW(), TRUE);
INSERT INTO items (category_id, name, date_added, visible) VALUES (2,'One plus', NOW(), TRUE);
INSERT INTO items (category_id, name, date_added, visible) VALUES (2,'iPhone 42', NOW(), TRUE);
INSERT INTO items (category_id, name, date_added, visible) VALUES (2,'Nokia 3310', NOW(), TRUE);
INSERT INTO items (category_id, name, date_added, visible) VALUES (4,'HP', NOW(), TRUE);
INSERT INTO items (category_id, name, date_added, visible) VALUES (5,'Huawei älykello', NOW(), TRUE);

INSERT INTO users (name, password) VALUES ('alpo','baloo');
INSERT INTO userinfo (user_id, puhelinnumero, paikkakunta, ptoimipaikka, sposti, osoite, kuvaus, nettisivu)
    VALUES (1,'0503694394','Helsinki','00140','alpo@gmail.com','Vuorimiehi 1','Luotettava myyjä!','www.alpo.fi');

INSERT INTO 
    iteminfo (item_id, user_id, price, kuvaus, ostetaan, picture)
    VALUES (8,1,12,'Hieno auto, paras',FALSE,'');
