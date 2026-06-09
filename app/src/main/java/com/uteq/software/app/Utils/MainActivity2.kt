package com.uteq.software.app.Utils

import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.Spinner
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import com.uteq.software.app.Adapters.AlumnoAdapter
import com.uteq.software.app.Models.Alumno
import com.uteq.software.app.Models.Materia
import com.uteq.software.app.R
import com.uteq.software.app.Services.SupabaseErrorHandler
import com.uteq.software.app.Services.SupabaseManager
import io.github.jan.supabase.exceptions.RestException
import io.github.jan.supabase.postgrest.from
import io.github.jan.supabase.postgrest.query.Order
import kotlinx.coroutines.launch

class MainActivity2 : AppCompatActivity() {

    private lateinit var spinnerSemestre: Spinner
    private lateinit var spinnerMaterias: Spinner
    private lateinit var listView: ListView

    private val categorias by lazy { resources.getStringArray(R.array.niveles).toList() }
    private var materiasFiltradas = listOf<Materia>()
    private var alumnos = ArrayList<Alumno>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main2)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        spinnerSemestre = findViewById(R.id.spinnerSemestre)
        spinnerMaterias = findViewById(R.id.spinnerMaterias)
        listView = findViewById(R.id.lvAlumnos)

        configurarSpinnerSemestre()
        configurarListeners()

        lifecycleScope.launch {
            cargarDatosIniciales()
        }
    }

    private fun configurarSpinnerSemestre() {
        val adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_item,
            categorias
        )
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerSemestre.adapter = adapter
        spinnerSemestre.setSelection(5)
    }

    private fun configurarListeners() {
        spinnerSemestre.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                lifecycleScope.launch {
                    cargarMaterias(position + 1)
                }
            }

            override fun onNothingSelected(parent: AdapterView<*>?) = Unit
        }

        spinnerMaterias.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                actualizarListaAlumnos()
            }

            override fun onNothingSelected(parent: AdapterView<*>?) = Unit
        }
    }

    private suspend fun cargarDatosIniciales() {
        try {
            alumnos = ArrayList(
                SupabaseManager.client
                    .from("alumnos")
                    .select {
                        order("nombres", Order.ASCENDING)
                    }
                    .decodeList<Alumno>()
            )
            val nivel = spinnerSemestre.selectedItemPosition + 1
            cargarMaterias(nivel)
        } catch (e: RestException) {
            SupabaseErrorHandler.show(this@MainActivity2, e)
        }
    }

    private suspend fun cargarMaterias(nivel: Int) {
        try {
            materiasFiltradas = SupabaseManager.client
                .from("materias")
                .select {
                    filter {
                        eq("nivel", nivel)
                    }
                    order("nombre", Order.ASCENDING)
                }
                .decodeList<Materia>()

            val nombres = materiasFiltradas.map { it.nombre ?: "" }
            val adapter = ArrayAdapter(
                this@MainActivity2,
                android.R.layout.simple_spinner_item,
                nombres
            )
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            spinnerMaterias.adapter = adapter
            actualizarListaAlumnos()
        } catch (e: RestException) {
            SupabaseErrorHandler.show(this@MainActivity2, e)
        }
    }

    private fun actualizarListaAlumnos() {
        listView.adapter = AlumnoAdapter(this, alumnos)
    }
}
