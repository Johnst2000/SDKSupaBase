package com.uteq.software.app.Utils

import android.os.Bundle
import android.view.View
import android.widget.EditText
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import com.uteq.software.app.Models.Alumno
import com.uteq.software.app.Services.SupabaseManager
import com.google.android.material.progressindicator.CircularProgressIndicator
import com.uteq.software.app.R
import io.github.jan.supabase.exceptions.RestException
import io.github.jan.supabase.postgrest.from
import io.github.jan.supabase.postgrest.query.Order
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val txtAlumnos = findViewById<EditText>(R.id.txtListaAlumnos)
        val progressMaterias =
            findViewById<CircularProgressIndicator>(R.id.progressMaterias)

        lifecycleScope.launch {
            progressMaterias.visibility = View.VISIBLE
            try {
                val alumnos = SupabaseManager.client
                    .from("alumnos")
                    .select {
                        order("nombres", Order.ASCENDING)
                    }
                    .decodeList<Alumno>()

                var texto = ""
                for (alumno in alumnos) {
                    texto += "Nombres: " + alumno.nombres + "\n"
                    texto += "Correo: " + alumno.correo + "\n"
                    texto += "TelÃ©fono: " + alumno.telefono + "\n"
                    texto += "Paralelo: " + alumno.paralelo + "\n\n"
                }

                txtAlumnos.setText(texto)

            } catch (e: RestException) {
                txtAlumnos.setText(e.description ?: e.message ?: "Error de Supabase")
            } catch (e: Exception) {
                txtAlumnos.setText(e.message ?: e.toString())
            } finally {
                progressMaterias.visibility = View.INVISIBLE
            }
        }
    }
}
