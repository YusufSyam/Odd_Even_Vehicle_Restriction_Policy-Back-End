-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 07, 2023 at 09:29 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `oevrp`
--

-- --------------------------------------------------------

--
-- Table structure for table `detector`
--

CREATE TABLE `detector` (
  `id` int(11) NOT NULL,
  `roadName` varchar(200) NOT NULL,
  `province` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `subDistrict` varchar(100) NOT NULL,
  `ward` varchar(100) NOT NULL,
  `roadImagePath` varchar(1000) NOT NULL,
  `description` varchar(2000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detector`
--

INSERT INTO `detector` (`id`, `roadName`, `province`, `city`, `subDistrict`, `ward`, `roadImagePath`, `description`) VALUES
(1, 'Andi Tonro', 'Sulawesi Selatan', 'Gowa', 'Somba Opu', 'Bonto-bontoa', 'files/img/andi-tonro.jpg', 'Jalan Andi Tonro merupakan jalanan yang membentang sekitar 10 KM. Jalan Andi Tonro merupakan pusat lalu lintas pada kelurahan bonto-bontoa, hal ini dikarenakan jalan ini berlokasi di pertengahan kecamatan somba opu, dan merupakan salah satu jalan yang menghubungkan Kota Makassar dan Kabupaten Gowa. Oleh karena itu jalan ini menjadi langganan kemacetan terutama pada saat jam pergi atau pulang kerja. Salah satu langkah pemerintah untuk mengatasi kemacetan pada jalan ini adalah dengan membuat jalan ini satu arah. Penerapan kebijakan ganjil genap juga berlaku pada jalan ini sejak 12 September 2021'),
(2, 'Jendral Sudirman', 'Jakarta', 'DKI Jakarta', '', '', 'files/img/jendral-sudirman.jpg', 'Jalan Jenderal Sudirman adalah salah satu jalan utama dan terkenal di Jakarta. Jalan ini merupakan salah satu akses utama menuju pusat bisnis dan keuangan Jakarta. Di sepanjang Jalan Jenderal Sudirman, Anda akan menemukan berbagai gedung pencakar langit, pusat perbelanjaan, hotel mewah, serta berbagai fasilitas komersial dan perkantoran.\nJalan Jenderal Sudirman juga terkenal dengan pemandangan yang indah pada malam hari, ketika gedung-gedungnya diterangi lampu-lampu yang cemerlang. Jalan ini sering digunakan untuk berbagai acara besar, seperti upacara peringatan nasional, lomba lari Jakarta Marathon, dan perayaan Tahun Baru yang meriah.\nSelain menjadi salah satu jalan utama di Jakarta, Jalan Jenderal Sudirman juga memiliki patung Pangeran Diponegoro yang terkenal sebagai salah satu landmark kota Jakarta. Jalan ini juga berperan penting dalam pengaturan lalu lintas ibu kota.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detector`
--
ALTER TABLE `detector`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detector`
--
ALTER TABLE `detector`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
