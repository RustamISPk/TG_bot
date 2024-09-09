-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: tg_bot
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `peoples`
--

DROP TABLE IF EXISTS `peoples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peoples` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Surname` varchar(30) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Patronymic` varchar(30) DEFAULT NULL,
  `Post` varchar(30) NOT NULL,
  `Project` varchar(100) NOT NULL,
  `Photo` varchar(100) DEFAULT NULL,
  `Date_Coming` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peoples`
--

LOCK TABLES `peoples` WRITE;
/*!40000 ALTER TABLE `peoples` DISABLE KEYS */;
INSERT INTO `peoples` VALUES (1,'Асафьев','Стас','Отсутствует','Директор','Управление компанией','AgACAgIAAxkBAAIRWWbensbdPj3Rsvbd9AG6jwblfqEBAAKt2zEb7xj4SlUd3tK6MNvQAQADAgADeQADNgQ','Отсутствует'),(2,'Стасяо','Сан','Отсутствует','Автоподборщик','Подбор автомобилей','AgACAgIAAxkBAAIRambenvEeF4geRSF5Ab86fDB80JOEAAKv2zEb7xj4SkesGAJ17S13AQADAgADeQADNgQ','Отсутствует'),(3,'Фон','Стасон','герр Кринге','Бухгалтер','Введение бух.учета','AgACAgIAAxkBAAIRfWbenyX883UJMT8MmYIzVq_BdO50AAKw2zEb7xj4SqcqOf52vBHeAQADAgADeAADNgQ','Отсутствует'),(4,'Фрасуа','Стасье','Жульен','Программист','Разработка и сопровождение сайта','AgACAgIAAxkBAAIRkWben1S7_ICKdGJ0ykWN-0E64c-GAAK12zEb7xj4SvjTpVMcaHBoAQADAgADbQADNgQ','Отсутствует'),(5,'Стасян','Ботан','Нагрузкович','Испытатель','Испытание безопасности подержанных автомобилей','AgACAgIAAxkBAAIRpmben5Gi1EJS8l9K5_t21kMt_npbAAK22zEb7xj4SvcIHCPDLyuaAQADAgADeQADNgQ','Отсутствует');
/*!40000 ALTER TABLE `peoples` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,'Программист'),(2,'Директор'),(3,'Автоподборщик'),(4,'Испытатель'),(5,'Бухгалтер');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-09 10:17:07
