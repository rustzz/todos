SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE `notes` (
  `id` int(11) NOT NULL,
  `hash` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `owner` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `checked` tinyint(1) NOT NULL DEFAULT 0,
  `parent` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `notes`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `notes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;
