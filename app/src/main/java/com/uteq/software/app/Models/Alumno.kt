package com.uteq.software.app.Models

import kotlinx.serialization.Serializable

@Serializable
data class Alumno(
    val id: Long,
    val nombres: String? = null,
    val correo: String? = null,
    val telefono: String? = null,
    val paralelo: String? = null,
    val foto: String? = null
)
