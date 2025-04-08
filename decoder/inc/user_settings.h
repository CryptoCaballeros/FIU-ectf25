/** @file user_settings.h
 *  @author Crypto Caballeros
 *  @brief Comprehensive side-channel resistant configuration for WolfSSL
 *  @date 2025
 */

// In decoder/inc/user_settings.h
#ifndef WOLFSSL_USER_SETTINGS_H
#define WOLFSSL_USER_SETTINGS_H

// Security enhancements
#define TFM_TIMING_RESISTANT       // Constant-time math operations
#define ECC_TIMING_RESISTANT       // ECC operations protected against timing attacks
#define HAVE_CONSTANT_TIME_IMPL    // Use constant-time implementations where available

// Memory/performance optimizations for embedded systems
#define WOLFSSL_SMALL_STACK        // Use less stack space
#define WOLFSSL_NO_MALLOC          // Avoid dynamic memory allocation
#define USE_FAST_MATH              // More efficient math implementation

// Specific cipher configurations for your use case
#define HAVE_AES_CBC               // You're using CBC mode
#define AES_MAX_KEY_SIZE 32        // Support 256-bit keys
#define NO_OLD_TLS                 // Disable older TLS versions
#define NO_DSA                     // Disable DSA algorithms
#define WOLFSSL_NO_SIGALGS         // Disable signature algorithms

// Add HMAC optimizations
#define HAVE_HKDF                  // Enable HKDF for key derivation
#define WOLFSSL_SHA384             // Enable SHA-384 (stronger alternative)

#endif /* WOLFSSL_USER_SETTINGS_H */

// #ifndef WOLFSSL_CONFIG_H
// #define WOLFSSL_CONFIG_H

// /* Core WolfSSL configuration */
// #define SINGLE_THREADED     /* No threading support needed */
// #define NO_FILESYSTEM
// #define NO_WRITEV           /* Embedded system without writev() */
// #define WOLFSSL_NO_CURRDIR  /* Don't use current directory */
// #define TIME_T_NOT_64BIT    /* Use 32-bit time_t */

// /* Optimization for embedded systems */
// #define WOLFSSL_SMALL_STACK
// #define SMALL_SESSION_CACHE
// #define NO_SESSION_CACHE
// #define WORD32_MASK 0xFFFFFFFF
// #define WORD64_MASK 0xFFFFFFFFFFFFFFFF

// /* Algorithm selection */
// #define WOLFSSL_AES_DIRECT    /* Direct AES operations */
// #define WOLFSSL_SHA256        /* Enables SHA 256 hash functions*/
// #define NO_RC4                /* Disable unused algorithms */
// #define NO_HC128
// #define NO_RABBIT
// #define NO_DSA
// #define NO_MD4

// /* Memory configuration */
// #define WOLFSSL_NO_MALLOC        /* Don't use dynamic memory allocation */
// #define WOLFSSL_STATIC_MEMORY    /* Use static memory buffers instead */

// /* Side-channel resistance - timing protections */
// #define TFM_TIMING_RESISTANT     /* Constant-time math operations */
// #define ECC_TIMING_RESISTANT     /* Protect ECC operations */
// #define WC_RSA_BLINDING          /* RSA blinding countermeasure */
// #define HAVE_CONSTANT_TIME_IMPL  /* Use constant-time implementations */

// /* Side-channel resistance - memory access protections */
// #define WC_NO_CACHE_RESISTANT    /* Avoid cache-based attacks */
// #define WC_NO_HARDEN            /* Disable hardware-specific optimizations that might leak */
// #define TFM_NO_ASM              /* Avoid assembly optimizations that might have timing variations */

// /* Specific algorithm hardening */
// #define AES_COUNTER_ONLY         /* AES in counter mode only, which is more resistant */
// #define GCM_TABLE_4BIT           /* Use smaller tables for AES-GCM to reduce cache footprint */

// #endif /* WOLFSSL_CONFIG_H */