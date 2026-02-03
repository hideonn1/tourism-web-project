-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2025 at 11:10 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bd_pjd`
--
CREATE DATABASE IF NOT EXISTS `bd_pjd` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `bd_pjd`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `rut` varchar(12) NOT NULL,
  `nombres` varchar(80) NOT NULL,
  `apellido_paterno` varchar(45) NOT NULL,
  `apellido_materno` varchar(45) NOT NULL,
  `email` varchar(150) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `fecha_registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `rut`, `nombres`, `apellido_paterno`, `apellido_materno`, `email`, `contraseña`, `rol`, `telefono`, `fecha_nacimiento`, `fecha_registro`) VALUES
(1, '12345678-9', 'Admin', 'Sistema', 'Principal', 'admin@admin.cl', '$2b$12$BpM6YxY9Mh6BaBllbSKO4OvH362uguAwyNqKrW3lvp9aeOHToPL4S', 'Administrador', '+56 9 1234 5678', '1990-01-01', '2025-11-29'),
(2, '98765432-1', 'Cliente', 'Prueba', 'Test', 'cliente@cliente.cl', '$2b$12$cbxQoXJlzE9aFW9NRVHeMuljXIHv85rVxmSkc2afQEAgAyJloLyrC', 'Cliente', '+56 9 8765 4321', '1995-06-15', '2025-11-29'),
(3, '20000000-5', 'Juanito', 'Navarrito', 'Carter', 'correo@correo.cl', '$2b$12$uJw6x0sA0xdRN3bWihkdV.aYEijnSnzqRAtOrrj.sFoMBXXFM0H.G', 'Cliente', '+56 9 3123 2323', '2000-09-23', '2025-12-01');

-- --------------------------------------------------------

--
-- NUEVA: Estructura de tabla para la tabla `password_resets`
--

CREATE TABLE `password_resets` (
  `id_reset` int(11) NOT NULL,
  `user_rut` varchar(12) NOT NULL,
  `token_hash` varchar(64) NOT NULL, -- Almacena SHA-256 del token
  `expires_at` datetime NOT NULL,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `destino`
--

CREATE TABLE `destino` (
  `id_destino` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `ciudad` varchar(150) NOT NULL,
  `pais` varchar(40) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `actividades_disponibles` varchar(255) NOT NULL,
  `costo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `destino`
--

INSERT INTO `destino` (`id_destino`, `nombre`, `ciudad`, `pais`, `descripcion`, `actividades_disponibles`, `costo`) VALUES
(1, 'Torres del Paine', 'Puerto Natales', 'Chile', 'Parque con picos de granito y glaciares. Ideal para el trekking patagónico.', 'Trekking, Observación de fauna, Kayak', 55000),
(2, 'Valle de la Luna', 'San Pedro de Atacama', 'Chile', 'Paisaje desértico que simula la superficie lunar, famoso por sus atardeceres.', 'Senderismo, Observación de estrellas, Tour en bicicleta', 30000),
(3, 'Valparaíso', 'Valparaíso', 'Chile', 'Ciudad puerto, Patrimonio de la Humanidad, conocida por sus cerros y ascensores.', 'Recorrido por cerros, Visita a museos, Ascensores históricos', 25000),
(4, 'Pucón', 'Pucón', 'Chile', 'Capital de la aventura en el sur, a orillas del Lago Villarrica y cerca del volcán.', 'Ascenso al Volcán, Rafting, Termas, Deportes náuticos', 38000),
(5, 'Isla de Pascua (Rapa Nui)', 'Hanga Roa', 'Chile', 'Isla polinésica famosa por los Moais. Centro de historia y cultura ancestral.', 'Visita a Moais, Buceo, Playa Anakena', 120000),
(6, 'Carretera Austral', 'Coyhaique', 'Chile', 'Ruta escénica que atraviesa la Patagonia, con fiordos y bosques.', 'Ruta en auto, Camping, Pesca con mosca', 70000),
(7, 'Santiago - Centro', 'Santiago', 'Chile', 'Capital de Chile, mezcla de edificios históricos, modernos y áreas verdes.', 'Museos, Palacio de La Moneda, Barrio Lastarria', 15000),
(8, 'Laguna San Rafael', 'Puerto Río Tranquilo', 'Chile', 'Famoso por el ventisquero San Rafael y su laguna azul con témpanos de hielo.', 'Navegación, Avistamiento de fauna marina', 90000),
(9, 'Viña del Mar', 'Viña del Mar', 'Chile', 'Ciudad jardín costera con amplias playas, parques y el famoso Reloj de Flores.', 'Playa, Muelle Vergara, Casino', 22000),
(10, 'Parque Nacional Lauca', 'Putre', 'Chile', 'Famoso por el Lago Chungará, uno de los más altos del mundo, y su fauna andina.', 'Observación de aves, Senderismo de altura, Vistas al Volcán Parinacota', 45000),
(11, 'Copacabana', 'Río de Janeiro', 'Brasil', 'Famosa playa en forma de media luna. Hogar del Cristo Redentor y el Pan de Azúcar.', 'Vóley playa, Natación, Teleférico, Visita al Corcovado', 50000),
(12, 'Cataratas del Iguazú', 'Foz do Iguaçu', 'Brasil', 'Impresionante conjunto de cascadas compartidas con Argentina, rodeadas de selva.', 'Recorridos en bote, Senderismo en el parque, Vistas panorámicas', 65000),
(13, 'Praia do Forte', 'Mata de São João', 'Brasil', 'Pueblo costero conocido por sus playas y la reserva de tortugas marinas (Proyecto Tamar).', 'Buceo, Proyecto Tamar, Relax en la playa', 40000),
(14, 'Salvador de Bahía', 'Salvador', 'Brasil', 'Capital cultural afrobrasileña, famosa por el Pelourinho y su vibrante música.', 'Explorar Pelourinho, Clases de Capoeira, Gastronomía local', 35000),
(15, 'Amazonas', 'Manaus', 'Brasil', 'Corazón de la selva amazónica, con biodiversidad única y el encuentro de los ríos.', 'Paseos en canoa, Avistamiento de fauna, Visita a tribus', 85000),
(16, 'Florianópolis', 'Florianópolis', 'Brasil', 'Isla con más de 40 playas, conocida por su surf, dunas y lagunas.', 'Surf, Sandboard en dunas, Senderismo costero', 30000),
(17, 'Búzios', 'Búzios', 'Brasil', 'Antiguo pueblo de pescadores popularizado por Brigitte Bardot, con hermosas calas.', 'Buceo, Paseos en barco, Vida nocturna en la Rua das Pedras', 42000),
(18, 'Ouro Preto', 'Ouro Preto', 'Brasil', 'Ciudad colonial Patrimonio de la Humanidad, rica en arquitectura barroca y minas de oro.', 'Visita a iglesias barrocas, Museos, Minas históricas', 28000),
(19, 'Recife y Olinda', 'Recife', 'Brasil', 'Recife (Venecia brasileña) y Olinda (centro histórico colonial y carnavalesco).', 'Visita a Olinda, Playas urbanas, Frevo y carnaval', 33000),
(20, 'Chapada Diamantina', 'Lençóis', 'Brasil', 'Parque Nacional de mesetas y cañones. Ideal para el ecoturismo.', 'Cascadas, Grutas, Trekking a mesetas', 48000),
(21, 'Glaciar Perito Moreno', 'El Calafate', 'Argentina', 'Masa de hielo espectacular conocida por sus rupturas y pasarelas de observación.', 'Excursión sobre el glaciar (Minitrekking), Navegación', 75000),
(22, 'Buenos Aires - Centro', 'Buenos Aires', 'Argentina', 'Capital cosmopolita. Famosa por el tango, teatros y su arquitectura europea.', 'Visita al Obelisco, Teatro Colón, San Telmo y Caminito', 20000),
(23, 'Ushuaia', 'Ushuaia', 'Argentina', 'La \"Ciudad del Fin del Mundo\". Punto de partida hacia la Antártida.', 'Tren del Fin del Mundo, Navegación por el Canal Beagle, Trekking en el Parque Nacional', 60000),
(24, 'Mendoza', 'Mendoza', 'Argentina', 'Región vitivinícola líder mundial, al pie de la Cordillera de los Andes.', 'Degustación de vinos, Tour por bodegas, Aventura en montaña', 35000),
(25, 'Puerto Madryn', 'Puerto Madryn', 'Argentina', 'Capital de las actividades subacuáticas y avistamiento de fauna marina (ballenas).', 'Avistamiento de Ballenas (en temporada), Buceo con lobos marinos', 52000),
(26, 'Bariloche', 'San Carlos de Bariloche', 'Argentina', 'Centro de esquí y turismo de aventura en la Patagonia andina. Famoso por sus chocolates.', 'Esquí, Senderismo, Circuito Chico, Chocolaterías', 40000),
(27, 'Salta y Jujuy', 'Salta', 'Argentina', 'Región del Norte con cultura andina, cerros de colores y tradiciones coloniales.', 'Quebrada de Humahuaca, Tren a las Nubes, Vinos de altura', 32000),
(28, 'Peninsula Valdés', 'Puerto Pirámides', 'Argentina', 'Reserva natural con colonias de elefantes marinos, pingüinos y aves.', 'Observación de fauna marina, Safaris terrestres', 58000),
(29, 'Córdoba', 'Córdoba', 'Argentina', 'Famosa por sus universidades, arquitectura jesuítica y su vida cultural.', 'Manzana Jesuítica, Visita a las Sierras, Museos', 27000),
(30, 'Rosario', 'Rosario', 'Argentina', 'Cuna de la bandera argentina, importante puerto y centro cultural.', 'Monumento a la Bandera, Paseo por la Costanera, Museos', 24000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquete_turistico`
--

CREATE TABLE `paquete_turistico` (
  `id_paquete_turistico` int(11) NOT NULL,
  `costo_paquete` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date NOT NULL,
  `modalidad` varchar(15) NOT NULL,
  `cupos` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `paquete_turistico`
--

INSERT INTO `paquete_turistico` (`id_paquete_turistico`, `costo_paquete`, `fecha_inicio`, `fecha_final`, `modalidad`, `cupos`) VALUES
(1, 60500, '2025-12-25', '2026-01-01', 'Nacional', 40),
(2, 121000, '2025-12-25', '2026-01-15', 'Nacional', 40),
(3, 145600, '2026-01-01', '2026-01-29', 'Nacional', 40),
(4, 198900, '2026-01-07', '2026-01-28', 'Nacional', 40),
(5, 312000, '2026-01-10', '2026-01-31', 'Nacional', 35),
(6, 266500, '2026-01-10', '2026-01-31', 'Nacional', 35),
(7, 120900, '2026-01-15', '2026-02-05', 'Nacional', 35),
(8, 204100, '2026-01-20', '2026-02-10', 'Nacional', 40),
(9, 152100, '2026-01-20', '2026-02-10', 'Nacional', 32),
(10, 204100, '2026-01-25', '2026-02-15', 'Nacional', 35),
(11, 65000, '2026-01-10', '2026-01-17', 'Internacional', 40),
(12, 201500, '2026-01-10', '2026-01-31', 'Internacional', 40),
(13, 195000, '2026-01-15', '2026-02-05', 'Internacional', 40),
(14, 133900, '2026-01-20', '2026-02-10', 'Internacional', 40),
(15, 237900, '2026-01-25', '2026-02-15', 'Internacional', 40),
(16, 201500, '2026-01-10', '2026-01-31', 'Internacional', 40),
(17, 165100, '2026-01-15', '2026-02-05', 'Internacional', 40),
(18, 152100, '2026-01-20', '2026-02-10', 'Internacional', 40),
(19, 152100, '2026-01-30', '2026-02-20', 'Internacional', 40),
(20, 326300, '2026-02-02', '2026-03-02', 'Internacional', 40),
(21, 269100, '2026-02-02', '2026-03-02', 'Internacional', 40);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva`
--

CREATE TABLE `reserva` (
  `id_reserva` int(11) NOT NULL,
  `estado` varchar(15) NOT NULL,
  `cupos` tinyint(4) NOT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reserva`
--

INSERT INTO `reserva` (`id_reserva`, `estado`, `cupos`, `id_usuario`) VALUES
(1, 'Pendiente', 3, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `destino_has_paquete_turistico`
--

CREATE TABLE `destino_has_paquete_turistico` (
  `destino_id_destino` int(11) NOT NULL,
  `paquete_turistico_id_paquete_turistico` int(11) NOT NULL,
  `fecha_salida` date NOT NULL,
  `fecha_llegada` date NOT NULL,
  `orden_visita` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva_has_paquete_turistico`
--

CREATE TABLE `reserva_has_paquete_turistico` (
  `reserva_id_reserva` int(11) NOT NULL,
  `paquete_turistico_id_paquete_turistico` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email_unique` (`email`),
  ADD UNIQUE KEY `rut_unique` (`rut`);

--
-- Indices de la tabla `password_resets`
--
ALTER TABLE `password_resets`
  ADD PRIMARY KEY (`id_reset`),
  ADD KEY `fk_pr_usuario_rut` (`user_rut`);

--
-- Indices de la tabla `destino`
--
ALTER TABLE `destino`
  ADD PRIMARY KEY (`id_destino`),
  ADD INDEX `idx_destino_pais` (`pais`),
  ADD INDEX `idx_destino_ciudad` (`ciudad`);

--
-- Indices de la tabla `paquete_turistico`
--
ALTER TABLE `paquete_turistico`
  ADD PRIMARY KEY (`id_paquete_turistico`),
  ADD INDEX `idx_paquete_modalidad` (`modalidad`),
  ADD INDEX `idx_paquete_fecha` (`fecha_inicio`);

--
-- Indices de la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD PRIMARY KEY (`id_reserva`),
  ADD KEY `fk_reserva_usuario` (`id_usuario`);

--
-- Indices de la tabla `destino_has_paquete_turistico`
--
ALTER TABLE `destino_has_paquete_turistico`
  ADD PRIMARY KEY (`destino_id_destino`,`paquete_turistico_id_paquete_turistico`),
  ADD KEY `fk_dhp_paquete` (`paquete_turistico_id_paquete_turistico`);

--
-- Indices de la tabla `reserva_has_paquete_turistico`
--
ALTER TABLE `reserva_has_paquete_turistico`
  ADD PRIMARY KEY (`reserva_id_reserva`,`paquete_turistico_id_paquete_turistico`),
  ADD KEY `fk_rhp_paquete` (`paquete_turistico_id_paquete_turistico`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `password_resets`
--
ALTER TABLE `password_resets`
  MODIFY `id_reset` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `destino`
--
ALTER TABLE `destino`
  MODIFY `id_destino` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `paquete_turistico`
--
ALTER TABLE `paquete_turistico`
  MODIFY `id_paquete_turistico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `reserva`
--
ALTER TABLE `reserva`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `password_resets`
--
ALTER TABLE `password_resets`
  ADD CONSTRAINT `fk_pr_usuario_rut` FOREIGN KEY (`user_rut`) REFERENCES `usuario` (`rut`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD CONSTRAINT `fk_reserva_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `destino_has_paquete_turistico`
--
ALTER TABLE `destino_has_paquete_turistico`
  ADD CONSTRAINT `fk_dhp_destino` FOREIGN KEY (`destino_id_destino`) REFERENCES `destino` (`id_destino`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_dhp_paquete` FOREIGN KEY (`paquete_turistico_id_paquete_turistico`) REFERENCES `paquete_turistico` (`id_paquete_turistico`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `reserva_has_paquete_turistico`
--
ALTER TABLE `reserva_has_paquete_turistico`
  ADD CONSTRAINT `fk_rhp_paquete` FOREIGN KEY (`paquete_turistico_id_paquete_turistico`) REFERENCES `paquete_turistico` (`id_paquete_turistico`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_rhp_reserva` FOREIGN KEY (`reserva_id_reserva`) REFERENCES `reserva` (`id_reserva`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;