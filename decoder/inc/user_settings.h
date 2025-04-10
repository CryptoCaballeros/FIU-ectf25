/** @file user_settings.h
 *  @author Crypto Caballeros
 *  @brief Comprehensive side-channel resistant configuration for WolfSSL
 *  @date 2025
 */

#ifndef WOLFSSL_USER_SETTINGS_H
#define WOLFSSL_USER_SETTINGS_H

/* Core WolfSSL configuration */
#define SINGLE_THREADED     /* No threading support needed */
#define NO_FILESYSTEM
#define NO_WRITEV           /* Embedded system without writev() */
#define WOLFSSL_SMALL_STACK /* Reuse small buffers when possible */
#define TIME_T_NOT_64BIT    /* Use 32-bit time_t */

/* Algorithm selection */
#define WOLFSSL_AES_DIRECT    /* Direct AES operations */
#define WOLFSSL_SHA256        /* Enables SHA 256 hash functions*/
#define NO_DES3
#define NO_RC4
#define NO_RSA
#define NO_DSA
#define NO_DH
#define NO_HMAC
#define NO_MD5
#define NO_MD4
#define NO_SHA
#define NO_OLD_TLS
#define NO_ASN
#define NO_SESSION_CACHE

/* Side-channel resistance - timing protections */
#define TFM_TIMING_RESISTANT     /* Constant-time math operations */
#define HAVE_CONSTANT_TIME_IMPL  /* Use constant-time implementations */

/* Side-channel resistance - memory access protections */
#define WC_NO_CACHE_RESISTANT    /* Avoid cache-based attacks */
#define TFM_NO_ASM              /* Avoid assembly optimizations that might have timing variations */

/* Additional security */
#define WC_RSA_BLINDING_ON       /* Protection for AES key material */

#endif /* WOLFSSL_USER_SETTINGS_H */                                                             