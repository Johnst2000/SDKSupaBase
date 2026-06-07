package com.uteq.software.app.Services

import io.github.jan.supabase.annotations.SupabaseInternal
import io.github.jan.supabase.createSupabaseClient
import io.github.jan.supabase.postgrest.Postgrest

object SupabaseManager {
    @OptIn(SupabaseInternal::class)
    val client by lazy {
        createSupabaseClient(
            supabaseUrl = "https://hnwamldwpxezbjtcmrup.supabase.co",
            supabaseKey = " "
        ) {
            install(Postgrest)
        }
    }
}
