-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: sarthtailor
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addcustomer`
--

DROP TABLE IF EXISTS `addcustomer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addcustomer` (
  `Reference_No` varchar(50) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Delivery` varchar(45) DEFAULT NULL,
  `Address` varchar(45) DEFAULT NULL,
  `Phone` varchar(10) DEFAULT NULL,
  `Shirt_Quantity` varchar(45) DEFAULT NULL,
  `Pant_Quantity` varchar(45) DEFAULT NULL,
  `Type_Of_Shirt` varchar(45) DEFAULT NULL,
  `Design_Of_Shirt` varchar(45) DEFAULT NULL,
  `Receiving_Date` varchar(45) DEFAULT NULL,
  `Submitted_Date` varchar(45) DEFAULT NULL,
  `Payment` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Reference_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addcustomer`
--

LOCK TABLES `addcustomer` WRITE;
/*!40000 ALTER TABLE `addcustomer` DISABLE KEYS */;
INSERT INTO `addcustomer` VALUES ('1370','Mahantesh Anadure','No','Dhotri','7028441334','2','1','Kurta','Apple Cut','11-09-2025','20/09/2025','500'),('6908','Samarth Yargle','No','Dhotri','8793932011','1','1','Full Shirt','Normal Cut','30-10-2025','31-10-2025','100'),('7264','Anil','Yes','dhotri','4598632110','1','2','Full Shirt','Apple Cut','19-09-2025','25-09-2025','5500'),('7378','Ganseh Anadure','Yes','Dhotri','8888357708','2','2','Full Shirt','Normal Cut','10-09-2025','30-09-2025','250'),('7576','Darshan','Yes','Dhotri','7020667700','2','2','Kurta','Apple Cut','23-12-2025','25-12-2025','100'),('9919','Onkar','Yes','Dhotri','7499419090','2','1','Kurta','Apple Cut','28-09-2025','30-09-2025','4000');
/*!40000 ALTER TABLE `addcustomer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES ('admin','admin','Your Happiness Reason?','Sister');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurement`
--

DROP TABLE IF EXISTS `measurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `measurement` (
  `Name` varchar(50) DEFAULT NULL,
  `Shirt_Cutting` varchar(45) DEFAULT NULL,
  `Pant_Cutting` varchar(45) DEFAULT NULL,
  `Sh_Length` varchar(45) DEFAULT NULL,
  `Sh_Chest` varchar(45) DEFAULT NULL,
  `Sh_Stomach` varchar(45) DEFAULT NULL,
  `Sh_Shoulder` varchar(45) DEFAULT NULL,
  `Sh_Sleeves` varchar(45) DEFAULT NULL,
  `Sh_Neck` varchar(45) DEFAULT NULL,
  `Sh_Cup` varchar(45) DEFAULT NULL,
  `Sh_Front` varchar(45) DEFAULT NULL,
  `Length` varchar(45) DEFAULT NULL,
  `Weist` varchar(45) DEFAULT NULL,
  `Seat` varchar(45) DEFAULT NULL,
  `Thigh` varchar(45) DEFAULT NULL,
  `Knee` varchar(45) DEFAULT NULL,
  `Bottom` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurement`
--

LOCK TABLES `measurement` WRITE;
/*!40000 ALTER TABLE `measurement` DISABLE KEYS */;
INSERT INTO `measurement` VALUES ('Darshan','No','Yes','23','56','87','45','11','20','69','45','45','8','4','1','23','33'),('Mahantesh Anadure','No','No','21','56','21','22','10','3','12','54','78','96','45','32','14','32');
/*!40000 ALTER TABLE `measurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_name` varchar(50) NOT NULL,
  `price` int NOT NULL,
  PRIMARY KEY (`product_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('Kurta',250),('Pant',200),('Shirt',300),('Tshirt',100);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-30 16:10:42
