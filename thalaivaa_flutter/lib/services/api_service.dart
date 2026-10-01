import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/models.dart';

class ApiService {
  static String get baseUrl {
    if (kIsWeb) {
      // In web browser, check if running on the same origin or dev server
      return '/api/v1';
    }
    return 'http://127.0.0.1:8000/api/v1';
  }

  static Map<String, String> _headers([String? token]) {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (token != null && token.isNotEmpty) {
      headers['Authorization'] = 'Bearer $token';
    }
    return headers;
  }

  /// Authenticate user against the database with email/phone & password
  static Future<Map<String, dynamic>> login({
    required String identifier,
    required String password,
  }) async {
    final url = Uri.parse('$baseUrl/auth/login');
    try {
      final response = await http.post(
        url,
        headers: _headers(),
        body: jsonEncode({
          'email_or_phone': identifier.trim(),
          'password': password,
        }),
      );

      final data = jsonDecode(response.body);
      if (response.statusCode == 200 && data['success'] == true) {
        return {
          'success': true,
          'token': data['token'],
          'user': UserModel.fromJson(data['user'], token: data['token']),
          'message': data['message'] ?? 'Authentication successful',
        };
      } else {
        return {
          'success': false,
          'message': data['message'] ?? 'Invalid credentials.',
        };
      }
    } catch (e) {
      // If relative URL fails in non-browser context, fallback to localhost
      if (kIsWeb && !baseUrl.startsWith('http')) {
        try {
          final fallbackUrl = Uri.parse('http://127.0.0.1:8000/api/v1/auth/login');
          final fallbackRes = await http.post(
            fallbackUrl,
            headers: _headers(),
            body: jsonEncode({
              'email_or_phone': identifier.trim(),
              'password': password,
            }),
          );
          final data = jsonDecode(fallbackRes.body);
          if (fallbackRes.statusCode == 200 && data['success'] == true) {
            return {
              'success': true,
              'token': data['token'],
              'user': UserModel.fromJson(data['user'], token: data['token']),
              'message': data['message'] ?? 'Authentication successful',
            };
          }
        } catch (_) {}
      }
      return {
        'success': false,
        'message': 'Failed to connect to backend server: $e',
      };
    }
  }

  /// OTP login verification against database
  static Future<Map<String, dynamic>> verifyOtp({
    required String phone,
    required String otp,
  }) async {
    final url = Uri.parse('$baseUrl/auth/otp/verify');
    try {
      final response = await http.post(
        url,
        headers: _headers(),
        body: jsonEncode({
          'phone': phone.trim(),
          'otp': otp.trim(),
        }),
      );

      final data = jsonDecode(response.body);
      if (response.statusCode == 200 && data['success'] == true) {
        return {
          'success': true,
          'token': data['token'],
          'user': UserModel.fromJson(data['user'], token: data['token']),
          'message': data['message'] ?? 'Authentication successful',
        };
      } else {
        return {
          'success': false,
          'message': data['message'] ?? 'Invalid OTP code.',
        };
      }
    } catch (e) {
      return {
        'success': false,
        'message': 'Network error: $e',
      };
    }
  }

  /// Fetch user-specific orders scoped to the authenticated token
  static Future<List<OrderModel>> fetchOrders(String token) async {
    final url = Uri.parse('$baseUrl/orders');
    try {
      final response = await http.get(url, headers: _headers(token));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final list = (data['data'] as List<dynamic>?) ?? [];
        return list.map((item) => OrderModel.fromJson(item)).toList();
      } else {
        throw Exception('Server returned ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      if (kIsWeb && !baseUrl.startsWith('http')) {
        try {
          final fallbackUrl = Uri.parse('http://127.0.0.1:8000/api/v1/orders');
          final fallbackRes = await http.get(fallbackUrl, headers: _headers(token));
          if (fallbackRes.statusCode == 200) {
            final data = jsonDecode(fallbackRes.body);
            final list = (data['data'] as List<dynamic>?) ?? [];
            return list.map((item) => OrderModel.fromJson(item)).toList();
          }
        } catch (_) {}
      }
      rethrow;
    }
  }

  /// Fetch single order details with ownership verification
  static Future<Map<String, dynamic>> fetchOrderDetail(String token, String orderId) async {
    final url = Uri.parse('$baseUrl/orders/$orderId');
    try {
      final response = await http.get(url, headers: _headers(token));
      return jsonDecode(response.body);
    } catch (e) {
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  /// Fetch active branches from database
  static Future<List<Branch>> fetchBranches() async {
    final url = Uri.parse('$baseUrl/branches');
    try {
      final response = await http.get(url, headers: _headers());
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final list = (data['data'] as List<dynamic>?) ?? [];
        return list.map((b) => Branch.fromJson(b)).toList();
      }
    } catch (_) {
      if (kIsWeb && !baseUrl.startsWith('http')) {
        try {
          final fallbackUrl = Uri.parse('http://127.0.0.1:8000/api/v1/branches');
          final fallbackRes = await http.get(fallbackUrl, headers: _headers());
          if (fallbackRes.statusCode == 200) {
            final data = jsonDecode(fallbackRes.body);
            final list = (data['data'] as List<dynamic>?) ?? [];
            return list.map((b) => Branch.fromJson(b)).toList();
          }
        } catch (_) {}
      }
    }
    return [];
  }

  /// Fetch active products from database
  static Future<List<Product>> fetchProducts({String? categoryId, String? search, bool? isVeg}) async {
    final queryParams = <String, String>{};
    if (categoryId != null && categoryId.isNotEmpty) queryParams['category_id'] = categoryId;
    if (search != null && search.isNotEmpty) queryParams['search'] = search;
    if (isVeg == true) queryParams['is_veg'] = '1';
    queryParams['per_page'] = '100';

    final uri = Uri.parse('$baseUrl/products').replace(queryParameters: queryParams);
    try {
      final response = await http.get(uri, headers: _headers());
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final list = (data['data'] as List<dynamic>?) ?? [];
        return list.map((p) => Product.fromJson(p)).toList();
      }
    } catch (_) {
      if (kIsWeb && !baseUrl.startsWith('http')) {
        try {
          final fallbackUri = Uri.parse('http://127.0.0.1:8000/api/v1/products').replace(queryParameters: queryParams);
          final fallbackRes = await http.get(fallbackUri, headers: _headers());
          if (fallbackRes.statusCode == 200) {
            final data = jsonDecode(fallbackRes.body);
            final list = (data['data'] as List<dynamic>?) ?? [];
            return list.map((p) => Product.fromJson(p)).toList();
          }
        } catch (_) {}
      }
    }
    return [];
  }

  /// Validate coupon against database
  static Future<Map<String, dynamic>> validateCoupon({
    required String code,
    required double subtotalInr,
    String? branchId,
  }) async {
    final url = Uri.parse('$baseUrl/coupons/validate');
    try {
      final response = await http.post(
        url,
        headers: _headers(),
        body: jsonEncode({
          'code': code.trim(),
          'subtotal_inr': subtotalInr,
          if (branchId != null) 'branch_id': branchId,
        }),
      );
      return jsonDecode(response.body);
    } catch (e) {
      if (kIsWeb && !baseUrl.startsWith('http')) {
        try {
          final fallbackUrl = Uri.parse('http://127.0.0.1:8000/api/v1/coupons/validate');
          final fallbackRes = await http.post(
            fallbackUrl,
            headers: _headers(),
            body: jsonEncode({
              'code': code.trim(),
              'subtotal_inr': subtotalInr,
              if (branchId != null) 'branch_id': branchId,
            }),
          );
          return jsonDecode(fallbackRes.body);
        } catch (_) {}
      }
      return {'success': false, 'message': 'Coupon validation failed: $e'};
    }
  }

  /// Submit order to database transactionally
  static Future<Map<String, dynamic>> createOrder({
    required Map<String, dynamic> payload,
    String? token,
  }) async {
    final url = Uri.parse('$baseUrl/orders');
    try {
      final response = await http.post(
        url,
        headers: _headers(token),
        body: jsonEncode(payload),
      );
      final data = jsonDecode(response.body);
      if (response.statusCode == 201 && data['success'] == true) {
        return {
          'success': true,
          'order': data['data'],
          'message': data['message'] ?? 'Order created successfully',
        };
      }
      return {
        'success': false,
        'message': data['message'] ?? 'Failed to place order',
      };
    } catch (e) {
      if (kIsWeb && !baseUrl.startsWith('http')) {
        try {
          final fallbackUrl = Uri.parse('http://127.0.0.1:8000/api/v1/orders');
          final fallbackRes = await http.post(
            fallbackUrl,
            headers: _headers(token),
            body: jsonEncode(payload),
          );
          final data = jsonDecode(fallbackRes.body);
          if (fallbackRes.statusCode == 201 && data['success'] == true) {
            return {
              'success': true,
              'order': data['data'],
              'message': data['message'] ?? 'Order created successfully',
            };
          }
        } catch (_) {}
      }
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  /// Revoke authenticated session/token
  static Future<bool> logout(String token) async {
    final url = Uri.parse('$baseUrl/auth/logout');
    try {
      final response = await http.post(url, headers: _headers(token));
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}
