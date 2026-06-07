package com.uteq.software.app.Services

import android.content.Context
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import io.github.jan.supabase.exceptions.RestException

object SupabaseErrorHandler {
    fun show(context: Context, e: RestException) {
        MaterialAlertDialogBuilder(context)
            .setTitle(e.error)
            .setMessage(e.description)
            .setIcon(android.R.drawable.ic_dialog_alert)
            .setPositiveButton("Aceptar", null)
            .show()
    }
}
