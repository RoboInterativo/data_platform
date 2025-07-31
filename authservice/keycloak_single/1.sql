CREATE TABLE `wiki`.`sessions` (
    `id` VARCHAR(255) NOT NULL,
    `data` BLOB NOT NULL,
    `expires` INT(11) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
