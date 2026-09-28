import os
import sys

providers_path = r'C:\Users\Admin\thalaivaa_flutter\lib\providers\app_providers.dart'
order_screen_path = r'C:\Users\Admin\thalaivaa_flutter\lib\features\order\order_screen.dart'

# 1. Update app_providers.dart to ensure clean dictionary keys & initial stage
with open(providers_path, 'r', encoding='utf-8') as f:
    providers_code = f.read()

# Add new dictionary keys for EN, HI, GU, TA
new_keys = {
    'en': """
      'assigningDriver': 'Assigning Delivery Partner',
      'assigningDriverSub': 'A partner will be assigned as soon as food is packed',
      'stage_out_pending_sub': 'Delivery partner will be assigned shortly',
      'delivered_by': 'Delivered by',
      'rateDelivery': 'Rate your delivery experience',
      'liveTrackingRadar': 'Live GPS Tracking',
      'driverHeadingYourWay': 'Rider is on the way to your doorstep',
      'verifiedDriver': 'Verified Delivery Partner',
      'trips': 'trips',
      'callDriver': 'Call Partner',
      'chatDriver': 'Chat with Partner',
      'quickChatHint': 'Quick message to rider...',
      'send': 'Send',
      'leaveAtDoor': 'Please leave at the door',
      'dontRingBell': 'Please do not ring the bell',
      'reachGate': 'Call when you reach the security gate',
      'distanceAway': '1.4 km away',
      'simStageConfirmed': 'Confirmed',
      'simStagePrep': 'Cooking',
      'simStageOut': 'On the Way',
      'simStageDelivered': 'Delivered',
      'orderStatusBadge': 'Live Tracking',
      'ratingThanks': 'Thank you for your rating!',
""",
    'hi': """
      'assigningDriver': 'डिलीवरी पार्टनर असाइन हो रहा है',
      'assigningDriverSub': 'खाना पैक होते ही पार्टनर असाइन कर दिया जाएगा',
      'stage_out_pending_sub': 'डिलीवरी पार्टनर जल्द ही असाइन किया जाएगा',
      'delivered_by': 'द्वारा डिलीवर किया गया',
      'rateDelivery': 'डिलीवरी अनुभव को रेट करें',
      'liveTrackingRadar': 'लाइव जीपीएस ट्रैकिंग',
      'driverHeadingYourWay': 'राइडर आपके पते की ओर आ रहा है',
      'verifiedDriver': 'सत्यापित डिलीवरी पार्टनर',
      'trips': 'ट्रिप्स',
      'callDriver': 'पार्टनर को कॉल करें',
      'chatDriver': 'पार्टनर से चैट करें',
      'quickChatHint': 'राइडर को त्वरित संदेश भेजें...',
      'send': 'भेजें',
      'leaveAtDoor': 'कृपया दरवाजे पर रखें',
      'dontRingBell': 'कृपया घंटी न बजाएं',
      'reachGate': 'गेट पर पहुंचकर कॉल करें',
      'distanceAway': '1.4 किमी दूर',
      'simStageConfirmed': 'स्वीकृत',
      'simStagePrep': 'तैयार हो रहा है',
      'simStageOut': 'रास्ते में',
      'simStageDelivered': 'डिलीवर हुआ',
      'orderStatusBadge': 'लाइव ट्रैकिंग',
      'ratingThanks': 'रेटिंग के लिए धन्यवाद!',
""",
    'gu': """
      'assigningDriver': 'ડિલિવરી પાર્ટનર ફાળવવામાં આવી રહ્યો છે',
      'assigningDriverSub': 'રસોઈ પેક થતાં જ ડિલિવરી પાર્ટનર ફાળવવામાં આવશે',
      'stage_out_pending_sub': 'ડિલિવરી પાર્ટનર ટૂંક સમયમાં ફાળવાશે',
      'delivered_by': 'દ્વારા ડિલિવર કરાયું',
      'rateDelivery': 'ડિલિવરી અનુભવને રેટ કરો',
      'liveTrackingRadar': 'લાઇવ જીપીએસ ટ્રેકિંગ',
      'driverHeadingYourWay': 'રાઇડર તમારા સરનામે આવી રહ્યો છે',
      'verifiedDriver': 'ચકાસાયેલ ડિલિવરી પાર્ટનર',
      'trips': 'ટ્રિપ્સ',
      'callDriver': 'કોલ કરો',
      'chatDriver': 'ચેટ કરો',
      'quickChatHint': 'રાઇડરને ઝડપી મેસેજ મોકલો...',
      'send': 'મોકલો',
      'leaveAtDoor': 'કૃપા કરીને દરવાજા પાસે મૂકો',
      'dontRingBell': 'કૃપા કરીને ઘંટડી ન વગાડો',
      'reachGate': 'સોસાયટીના ગેટ પર પહોંચીને કોલ કરો',
      'distanceAway': '1.4 કિમી દૂર',
      'simStageConfirmed': 'સ્વીકારાયો',
      'simStagePrep': 'રસોઈ ચાલુ',
      'simStageOut': 'રસ્તામાં',
      'simStageDelivered': 'ડિલિવર થયું',
      'orderStatusBadge': 'લાઇવ ટ્રેકિંગ',
      'ratingThanks': 'રેટિંગ આપવા બદલ આભાર!',
""",
    'ta': """
      'assigningDriver': 'டெலிவரி பார்ட்னர் ஒதுக்கப்படுகிறார்',
      'assigningDriverSub': 'உணவு பேக் செய்யப்பட்டவுடன் பார்ட்னர் நியமிக்கப்படுவார்',
      'stage_out_pending_sub': 'டெலிவரி பார்ட்னர் விரைவில் ஒதுக்கப்படுவார்',
      'delivered_by': 'டெலிவரி செய்தவர்',
      'rateDelivery': 'டெலிவரி அனுபவத்தை மதிப்பிடுங்கள்',
      'liveTrackingRadar': 'நேரலை ஜிபிஎஸ் டிராக்கிங்',
      'driverHeadingYourWay': 'டெலிவரி பார்ட்னர் உங்கள் இருப்பிடத்திற்கு வருகிறார்',
      'verifiedDriver': 'சரிபார்க்கப்பட்ட டெலிவரி பார்ட்னர்',
      'trips': 'பயணங்கள்',
      'callDriver': 'அழைக்க',
      'chatDriver': 'செய்தி அனுப்ப',
      'quickChatHint': 'விரைவு செய்தி அனுப்பவும்...',
      'send': 'அனுப்புக',
      'leaveAtDoor': 'தயவுசெய்து வாசலில் வைக்கவும்',
      'dontRingBell': 'தயவுசெய்து மணியை அடிக்க வேண்டாம்',
      'reachGate': 'கேட்டை அடைந்ததும் அழைக்கவும்',
      'distanceAway': '1.4 கிமீ தொலைவில்',
      'simStageConfirmed': 'உறுதியானது',
      'simStagePrep': 'சமையல்',
      'simStageOut': 'வழியில்',
      'simStageDelivered': 'முடிந்தது',
      'orderStatusBadge': 'நேரலை டிராக்கிங்',
      'ratingThanks': 'உங்கள் மதிப்பீட்டிற்கு நன்றி!',
"""
}

for lang, additions in new_keys.items():
    marker = f"'{lang}': {{"
    if marker in providers_code:
        if "'assigningDriver':" not in providers_code[providers_code.find(marker):providers_code.find(marker)+4000]:
            providers_code = providers_code.replace(marker, marker + additions)

with open(providers_path, 'w', encoding='utf-8') as f:
    f.write(providers_code)
print("Updated app_providers.dart successfully.")

# 2. Write the complete, top-tier SaaS OrderScreen in order_screen.dart
order_screen_content = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/cart_item.dart';
import '../../providers/app_providers.dart';

// Live Rating Provider for completed deliveries
final deliveryRatingProvider = StateProvider<int>((ref) => 5);
final deliveryFeedbackSentProvider = StateProvider<bool>((ref) => false);

class OrderScreen extends ConsumerWidget {
  const OrderScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final orders = ref.watch(ordersProvider);
    final stage = ref.watch(liveTrackingStageProvider);
    final eta = ref.watch(etaMinutesProvider);
    final rider = ref.watch(activeRiderProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final selectedAddress = ref.watch(selectedAddressProvider);
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.radar_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
            ),
            const SizedBox(width: 10),
            Text(
              tr('trackingTitle'),
              style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 18),
            ),
          ],
        ),
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 16, top: 10, bottom: 10),
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: stage == LiveTrackingStage.delivered
                  ? ThalaivaaTheme.vegGreen.withValues(alpha: 0.15)
                  : ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: stage == LiveTrackingStage.delivered
                    ? ThalaivaaTheme.vegGreen.withValues(alpha: 0.4)
                    : ThalaivaaTheme.brandAmber.withValues(alpha: 0.4),
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: stage == LiveTrackingStage.delivered ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.brandAmber,
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 6),
                Text(
                  stage == LiveTrackingStage.delivered ? tr('simStageDelivered') : '#ORD-1001',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w900,
                    color: stage == LiveTrackingStage.delivered ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.brandAmber,
                  ),
                ),
              ],
            ),
          ),
        ],
        elevation: 0,
        backgroundColor: cardBg,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 40),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // 1. Enterprise Interactive Simulation Stage Selector
                _buildSimulationStageSelector(context, ref, stage, tr, isDark),

                const SizedBox(height: 16),

                // 2. High-Tech Animated Radar / Live Route Map Visualizer
                _buildLiveMapRadarVisualizer(context, stage, rider, selectedBranch, selectedAddress, tr, isDark),

                const SizedBox(height: 16),

                // 3. ETA & Dynamic Status Banner Hero Card
                _buildEtaHeroCard(stage, eta, tr, isDark),

                const SizedBox(height: 16),

                // 4. Conditional Driver / Delivery Partner Card
                // STRICT REQUIREMENT: Driver details ONLY appear when out for delivery (or delivered summary)
                if (stage == LiveTrackingStage.onTheWay)
                  _buildActiveDriverCard(context, rider, tr, isDark)
                else if (stage == LiveTrackingStage.delivered)
                  _buildDeliveredSummaryCard(context, ref, rider, tr, isDark)
                else
                  _buildPendingDriverCard(tr, isDark),

                const SizedBox(height: 16),

                // 5. 4-Stage Visual Progress Timeline
                _buildProgressTimeline(stage, rider, selectedBranch, selectedAddress, tr, isDark, cardBg, cardBorder),

                const SizedBox(height: 16),

                // 6. Order Summary & Itemized Breakdown
                _buildOrderSummaryCard(orders, selectedBranch, selectedAddress, tr, isDark, cardBg, cardBorder, ref),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // 1. Interactive 4-Stage Simulation Selector
  Widget _buildSimulationStageSelector(
    BuildContext context,
    WidgetRef ref,
    LiveTrackingStage currentStage,
    String Function(String) tr,
    bool isDark,
  ) {
    final stages = [
      {'stage': LiveTrackingStage.confirmed, 'label': tr('simStageConfirmed'), 'eta': 22, 'icon': Icons.receipt_long_rounded},
      {'stage': LiveTrackingStage.preparing, 'label': tr('simStagePrep'), 'eta': 14, 'icon': Icons.soup_kitchen_rounded},
      {'stage': LiveTrackingStage.onTheWay, 'label': tr('simStageOut'), 'eta': 8, 'icon': Icons.two_wheeler_rounded},
      {'stage': LiveTrackingStage.delivered, 'label': tr('simStageDelivered'), 'eta': 0, 'icon': Icons.check_circle_rounded},
    ];

    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF161E2E) : const Color(0xFFEDF2F7),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: isDark ? const Color(0xFF2D3748) : const Color(0xFFCBD5E1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(Icons.alt_route_rounded, size: 14, color: ThalaivaaTheme.brandAmber),
                    const SizedBox(width: 6),
                    Text(
                      'SIMULATE TRACKING STAGES',
                      style: TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 1.0,
                        color: isDark ? Colors.white70 : const Color(0xFF475569),
                      ),
                    ),
                  ],
                ),
                Text(
                  'Tap any state to test UI',
                  style: TextStyle(fontSize: 10, color: isDark ? Colors.white38 : Colors.grey),
                ),
              ],
            ),
          ),
          const SizedBox(height: 6),
          Row(
            children: stages.map((item) {
              final stage = item['stage'] as LiveTrackingStage;
              final isSelected = currentStage == stage;
              final label = item['label'] as String;
              final icon = item['icon'] as IconData;
              final eta = item['eta'] as int;

              return Expanded(
                child: GestureDetector(
                  onTap: () {
                    ref.read(liveTrackingStageProvider.notifier).state = stage;
                    ref.read(etaMinutesProvider.notifier).state = eta;
                  },
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 250),
                    margin: const EdgeInsets.symmetric(horizontal: 3),
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    decoration: BoxDecoration(
                      color: isSelected
                          ? ThalaivaaTheme.primaryDeep
                          : (isDark ? const Color(0xFF1E293B) : Colors.white),
                      borderRadius: BorderRadius.circular(12),
                      boxShadow: isSelected
                          ? [
                              BoxShadow(
                                color: ThalaivaaTheme.primaryDeep.withValues(alpha: 0.4),
                                blurRadius: 8,
                                offset: const Offset(0, 2),
                              )
                            ]
                          : null,
                      border: Border.all(
                        color: isSelected
                            ? ThalaivaaTheme.brandAmber
                            : (isDark ? Colors.transparent : const Color(0xFFE2E8F0)),
                        width: isSelected ? 1.5 : 1.0,
                      ),
                    ),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          icon,
                          size: 16,
                          color: isSelected ? Colors.white : (isDark ? Colors.white60 : Colors.black54),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          label,
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: isSelected ? FontWeight.w900 : FontWeight.w600,
                            color: isSelected ? Colors.white : (isDark ? Colors.white70 : const Color(0xFF334155)),
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  // 2. High-Tech Animated Radar / Live Route Map Visualizer
  Widget _buildLiveMapRadarVisualizer(
    BuildContext context,
    LiveTrackingStage stage,
    DeliveryRider rider,
    dynamic branch,
    dynamic address,
    String Function(String) tr,
    bool isDark,
  ) {
    double progress = 0.15;
    if (stage == LiveTrackingStage.preparing) progress = 0.40;
    if (stage == LiveTrackingStage.onTheWay) progress = 0.78;
    if (stage == LiveTrackingStage.delivered) progress = 1.0;

    return Container(
      height: 190,
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF0F172A) : const Color(0xFFE2E8F0),
        borderRadius: BorderRadius.circular(22),
        border: Border.all(
          color: isDark ? const Color(0xFF334155) : const Color(0xFFCBD5E1),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: isDark ? 0.35 : 0.08),
            blurRadius: 16,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(21),
        child: Stack(
          children: [
            // Ambient stylized grid & map graphic background
            CustomPaint(
              size: const Size(double.infinity, 190),
              painter: _SaaSRoutePainter(
                progress: progress,
                isDark: isDark,
                stage: stage,
              ),
            ),

            // Top Status Overlay Banner
            Positioned(
              top: 12,
              left: 12,
              right: 12,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: (isDark ? Colors.black : Colors.white).withValues(alpha: 0.85),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(
                        color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.5),
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 8,
                          height: 8,
                          decoration: const BoxDecoration(
                            color: ThalaivaaTheme.brandAmber,
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 6),
                        Text(
                          tr('liveTrackingRadar'),
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w900,
                            color: isDark ? Colors.white : Colors.black87,
                          ),
                        ),
                      ],
                    ),
                  ),
                  if (stage == LiveTrackingStage.onTheWay)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(
                        color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.9),
                        borderRadius: BorderRadius.circular(10),
                        boxShadow: [
                          BoxShadow(
                            color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.3),
                            blurRadius: 6,
                          ),
                        ],
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.near_me_rounded, color: Colors.white, size: 12),
                          const SizedBox(width: 4),
                          Text(
                            tr('distanceAway'),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 11,
                              fontWeight: FontWeight.w900,
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),

            // Bottom Route Locations Bar
            Positioned(
              bottom: 12,
              left: 12,
              right: 12,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: (isDark ? const Color(0xFF1E293B) : Colors.white).withValues(alpha: 0.92),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(
                    color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                  ),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.storefront_rounded, color: ThalaivaaTheme.brandAmber, size: 16),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        branch.name,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: isDark ? Colors.white70 : const Color(0xFF1E293B),
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const Icon(Icons.arrow_forward_rounded, size: 14, color: Colors.grey),
                    const SizedBox(width: 6),
                    const Icon(Icons.home_pin_rounded, color: ThalaivaaTheme.vegGreen, size: 16),
                    const SizedBox(width: 4),
                    Expanded(
                      child: Text(
                        address.label,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: isDark ? Colors.white70 : const Color(0xFF1E293B),
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // 3. ETA & Dynamic Status Banner Hero Card
  Widget _buildEtaHeroCard(LiveTrackingStage stage, int eta, String Function(String) tr, bool isDark) {
    String headline;
    String sub;
    IconData iconData;

    switch (stage) {
      case LiveTrackingStage.confirmed:
        headline = '$eta ${tr('mins')}';
        sub = tr('stage_confirmed_sub');
        iconData = Icons.receipt_long_rounded;
        break;
      case LiveTrackingStage.preparing:
        headline = '$eta ${tr('mins')}';
        sub = tr('stage_prep_sub');
        iconData = Icons.outdoor_grill_rounded;
        break;
      case LiveTrackingStage.onTheWay:
        headline = '$eta ${tr('mins')}';
        sub = tr('driverHeadingYourWay');
        iconData = Icons.two_wheeler_rounded;
        break;
      case LiveTrackingStage.delivered:
        headline = tr('stage_delivered_title');
        sub = tr('stage_delivered_sub');
        iconData = Icons.verified_rounded;
        break;
    }

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: isDark
              ? [const Color(0xFF1E1B4B), const Color(0xFF2E1065)]
              : [const Color(0xFFFFF7ED), const Color(0xFFFFEDD5)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.4), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: isDark ? 0.3 : 0.05),
            blurRadius: 14,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: (stage == LiveTrackingStage.delivered ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.brandAmber)
                          .withValues(alpha: 0.2),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      iconData,
                      color: stage == LiveTrackingStage.delivered ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.brandAmber,
                      size: 26,
                    ),
                  ),
                  const SizedBox(width: 14),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        tr('estimatedDelivery').toUpperCase(),
                        style: TextStyle(
                          fontSize: 10,
                          color: isDark ? Colors.white60 : Colors.black54,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 0.8,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        headline,
                        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
                      ),
                    ],
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.4)),
                ),
                child: Text(
                  tr('onTime'),
                  style: const TextStyle(
                    color: ThalaivaaTheme.vegGreen,
                    fontWeight: FontWeight.w900,
                    fontSize: 11,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: (isDark ? Colors.black : Colors.white).withValues(alpha: 0.4),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Row(
              children: [
                const Icon(Icons.info_outline_rounded, size: 14, color: ThalaivaaTheme.brandAmber),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    sub,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: isDark ? Colors.white70 : const Color(0xFF475569),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // 4A. Pending Driver Card (Stages 1 & 2: NO DRIVER NAME REVEALED)
  Widget _buildPendingDriverCard(String Function(String) tr, bool isDark) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(
          color: isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0),
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: (isDark ? Colors.white10 : const Color(0xFFF1F5F9)),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.delivery_dining_rounded, color: Colors.grey, size: 24),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      tr('assigningDriver'),
                      style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 13),
                    ),
                    const SizedBox(width: 6),
                    SizedBox(
                      width: 12,
                      height: 12,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.8),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 3),
                Text(
                  tr('assigningDriverSub'),
                  style: TextStyle(
                    fontSize: 11,
                    color: isDark ? Colors.white54 : const Color(0xFF64748B),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // 4B. Active Driver Card (Stage 3: Out for Delivery — FULL DRIVER DETAILS)
  Widget _buildActiveDriverCard(
    BuildContext context,
    DeliveryRider rider,
    String Function(String) tr,
    bool isDark,
  ) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.5), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.1),
            blurRadius: 14,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            children: [
              Stack(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                      shape: BoxShape.circle,
                      border: Border.all(color: ThalaivaaTheme.brandAmber, width: 2),
                    ),
                    child: Text(rider.photoEmoji, style: const TextStyle(fontSize: 24)),
                  ),
                  Positioned(
                    bottom: 0,
                    right: 0,
                    child: Container(
                      padding: const EdgeInsets.all(2),
                      decoration: const BoxDecoration(
                        color: ThalaivaaTheme.vegGreen,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.check, size: 10, color: Colors.white),
                    ),
                  ),
                ],
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          rider.name,
                          style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15),
                        ),
                        const SizedBox(width: 6),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(6),
                          ),
                          child: Text(
                            tr('verifiedDriver'),
                            style: const TextStyle(
                              fontSize: 9,
                              fontWeight: FontWeight.w900,
                              color: ThalaivaaTheme.vegGreen,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 3),
                    Text(
                      '${rider.vehicle}  |  ★ ${rider.rating} (${rider.completedTrips} ${tr('trips')})',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        color: isDark ? Colors.white60 : Colors.black54,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () => _showCallDialog(context, rider, tr, isDark),
                  icon: const Icon(Icons.phone_rounded, size: 16, color: ThalaivaaTheme.vegGreen),
                  label: Text(
                    tr('callDriver'),
                    style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 12),
                  ),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: ThalaivaaTheme.vegGreen,
                    side: BorderSide(color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.5)),
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: () => _showChatDialog(context, rider, tr, isDark),
                  icon: const Icon(Icons.chat_bubble_rounded, size: 16),
                  label: Text(
                    tr('chatDriver'),
                    style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 12),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: ThalaivaaTheme.brandAmber,
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // 4C. Delivered State Driver Summary & 5-Star Rating Card
  Widget _buildDeliveredSummaryCard(
    BuildContext context,
    WidgetRef ref,
    DeliveryRider rider,
    String Function(String) tr,
    bool isDark,
  ) {
    final rating = ref.watch(deliveryRatingProvider);
    final feedbackSent = ref.watch(deliveryFeedbackSentProvider);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.5), width: 1.5),
      ),
      child: Column(
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.verified_rounded, color: ThalaivaaTheme.vegGreen, size: 22),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${tr('delivered_by')} ${rider.name}',
                      style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 14),
                    ),
                    Text(
                      tr('rateDelivery'),
                      style: TextStyle(
                        fontSize: 11,
                        color: isDark ? Colors.white60 : Colors.black54,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          if (!feedbackSent) ...[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(5, (index) {
                final starNum = index + 1;
                return IconButton(
                  icon: Icon(
                    starNum <= rating ? Icons.star_rounded : Icons.star_border_rounded,
                    color: ThalaivaaTheme.brandAmber,
                    size: 32,
                  ),
                  onPressed: () {
                    ref.read(deliveryRatingProvider.notifier).state = starNum;
                    ref.read(deliveryFeedbackSentProvider.notifier).state = true;
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(tr('ratingThanks')),
                        backgroundColor: ThalaivaaTheme.vegGreen,
                      ),
                    );
                  },
                );
              }),
            ),
          ] else ...[
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.check_circle_rounded, color: ThalaivaaTheme.vegGreen, size: 16),
                  const SizedBox(width: 6),
                  Text(
                    '★ $rating / 5 — ${tr('ratingThanks')}',
                    style: const TextStyle(
                      color: ThalaivaaTheme.vegGreen,
                      fontWeight: FontWeight.w800,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  // 5. 4-Stage Visual Progress Timeline
  Widget _buildProgressTimeline(
    LiveTrackingStage stage,
    DeliveryRider rider,
    dynamic branch,
    dynamic address,
    String Function(String) tr,
    bool isDark,
    Color cardBg,
    Color cardBorder,
  ) {
    // Dynamic Subtitle for Stage 3 (Strictly Hides Driver Name unless out for delivery)
    final stage3Subtitle = (stage == LiveTrackingStage.onTheWay || stage == LiveTrackingStage.delivered)
        ? '${tr('stage_out_sub')} • ${rider.name}'
        : tr('stage_out_pending_sub');

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.timeline_rounded, size: 16, color: ThalaivaaTheme.brandAmber),
              const SizedBox(width: 8),
              Text(
                'ORDER JOURNEY',
                style: TextStyle(
                  fontWeight: FontWeight.w900,
                  fontSize: 12,
                  letterSpacing: 0.8,
                  color: isDark ? Colors.white70 : const Color(0xFF475569),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          _buildTimelineRow(
            icon: Icons.check_circle_rounded,
            title: tr('stage_confirmed_title'),
            subtitle: '${tr('stage_confirmed_sub')} (${branch.name})',
            isDone: true,
            isCurrent: stage == LiveTrackingStage.confirmed,
            isDark: isDark,
          ),
          _buildTimelineDivider(isDone: stage != LiveTrackingStage.confirmed, isDark: isDark),
          _buildTimelineRow(
            icon: Icons.soup_kitchen_rounded,
            title: tr('stage_prep_title'),
            subtitle: tr('stage_prep_sub'),
            isDone: stage == LiveTrackingStage.preparing || stage == LiveTrackingStage.onTheWay || stage == LiveTrackingStage.delivered,
            isCurrent: stage == LiveTrackingStage.preparing,
            isDark: isDark,
          ),
          _buildTimelineDivider(isDone: stage == LiveTrackingStage.onTheWay || stage == LiveTrackingStage.delivered, isDark: isDark),
          _buildTimelineRow(
            icon: Icons.two_wheeler_rounded,
            title: tr('stage_out_title'),
            subtitle: stage3Subtitle,
            isDone: stage == LiveTrackingStage.onTheWay || stage == LiveTrackingStage.delivered,
            isCurrent: stage == LiveTrackingStage.onTheWay,
            isDark: isDark,
          ),
          _buildTimelineDivider(isDone: stage == LiveTrackingStage.delivered, isDark: isDark),
          _buildTimelineRow(
            icon: Icons.celebration_rounded,
            title: tr('stage_delivered_title'),
            subtitle: '${tr('stage_delivered_sub')} (${address.addressLine})',
            isDone: stage == LiveTrackingStage.delivered,
            isCurrent: stage == LiveTrackingStage.delivered,
            isDark: isDark,
          ),
        ],
      ),
    );
  }

  Widget _buildTimelineRow({
    required IconData icon,
    required String title,
    required String subtitle,
    required bool isDone,
    required bool isCurrent,
    required bool isDark,
  }) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(7),
          decoration: BoxDecoration(
            color: isDone
                ? ThalaivaaTheme.vegGreen
                : (isDark ? Colors.white10 : const Color(0xFFE2E8F0)),
            shape: BoxShape.circle,
            border: isCurrent
                ? Border.all(color: ThalaivaaTheme.brandAmber, width: 3)
                : null,
            boxShadow: isCurrent
                ? [
                    BoxShadow(
                      color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.5),
                      blurRadius: 8,
                    )
                  ]
                : null,
          ),
          child: Icon(
            icon,
            size: 15,
            color: isDone ? Colors.white : (isDark ? Colors.white38 : Colors.grey),
          ),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 13,
                  color: isDone
                      ? (isDark ? Colors.white : const Color(0xFF0F172A))
                      : (isDark ? Colors.white38 : Colors.grey),
                ),
              ),
              const SizedBox(height: 2),
              Text(
                subtitle,
                style: TextStyle(
                  fontSize: 11,
                  color: isDark ? Colors.white54 : const Color(0xFF64748B),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildTimelineDivider({required bool isDone, required bool isDark}) {
    return Container(
      margin: const EdgeInsets.only(left: 14),
      width: 2.5,
      height: 24,
      color: isDone ? ThalaivaaTheme.vegGreen : (isDark ? Colors.white10 : const Color(0xFFE2E8F0)),
    );
  }

  // 6. Order Summary & Itemized Breakdown
  Widget _buildOrderSummaryCard(
    List<dynamic> orders,
    dynamic branch,
    dynamic address,
    String Function(String) tr,
    bool isDark,
    Color cardBg,
    Color cardBorder,
    WidgetRef ref,
  ) {
    if (orders.isEmpty) {
      // Provide default fallback preview items
      return Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: cardBg,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(color: cardBorder),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(tr('orderSummary'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                const Text('#ORD-1001', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: ThalaivaaTheme.brandAmber)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: const [
                Text('1x Ghee Podi Roast Dosa', style: TextStyle(fontSize: 13)),
                Text('₹189.00', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: const [
                Text('1x Filter Kaapi Classic', style: TextStyle(fontSize: 13)),
                Text('₹79.00', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
              ],
            ),
            const Divider(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(tr('totalPaid'), style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 14)),
                const Text(
                  '₹268.00',
                  style: TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: ThalaivaaTheme.brandAmber),
                ),
              ],
            ),
          ],
        ),
      );
    }

    final order = orders.first;
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(tr('orderSummary'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
              Text(order.orderId, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: ThalaivaaTheme.brandAmber)),
            ],
          ),
          const SizedBox(height: 10),
          ...order.items.map((item) {
            final localizedInfo = ref.watch(localizedDishInfoProvider(item.product));
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('${item.quantity}x ${localizedInfo.name}', style: const TextStyle(fontSize: 13)),
                  Text(ThalaivaaTheme.formatInr(item.totalPrice), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                ],
              ),
            );
          }).toList(),
          const Divider(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(tr('totalPaid'), style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 14)),
              Text(
                ThalaivaaTheme.formatInr(order.grandTotal),
                style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: ThalaivaaTheme.brandAmber),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // Action Dialog: Call Driver
  void _showCallDialog(BuildContext context, DeliveryRider rider, String Function(String) tr, bool isDark) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            const Icon(Icons.phone_in_talk_rounded, color: ThalaivaaTheme.vegGreen),
            const SizedBox(width: 8),
            Text(tr('callDriver'), style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('${rider.name} • ${rider.vehicle}', style: const TextStyle(fontWeight: FontWeight.w700)),
            const SizedBox(height: 6),
            Text('Direct Phone: ${rider.phone}', style: const TextStyle(fontSize: 13, color: Colors.grey)),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
          ElevatedButton.icon(
            onPressed: () {
              Navigator.pop(ctx);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('Dialing ${rider.phone}...'),
                  backgroundColor: ThalaivaaTheme.vegGreen,
                ),
              );
            },
            icon: const Icon(Icons.call, size: 16),
            label: const Text('Connect Call'),
            style: ElevatedButton.styleFrom(
              backgroundColor: ThalaivaaTheme.vegGreen,
              foregroundColor: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  // Action Dialog: In-App Chat Modal
  void _showChatDialog(BuildContext context, DeliveryRider rider, String Function(String) tr, bool isDark) {
    final quickMessages = [
      tr('leaveAtDoor'),
      tr('dontRingBell'),
      tr('reachGate'),
    ];

    showModalBottomSheet(
      context: context,
      backgroundColor: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.fromLTRB(18, 18, 18, 30),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(rider.photoEmoji, style: const TextStyle(fontSize: 22)),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(rider.name, style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15)),
                      Text('Online • ${rider.vehicle}', style: const TextStyle(fontSize: 11, color: Colors.grey)),
                    ],
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.pop(ctx),
                ),
              ],
            ),
            const Divider(height: 20),
            Text(
              'QUICK INSTRUCTIONS',
              style: TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w900,
                color: isDark ? Colors.white60 : Colors.black54,
                letterSpacing: 0.8,
              ),
            ),
            const SizedBox(height: 10),
            ...quickMessages.map((msg) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(10),
                    onTap: () {
                      Navigator.pop(ctx);
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Message sent to ${rider.name}: "$msg"'),
                          backgroundColor: ThalaivaaTheme.brandAmber,
                        ),
                      );
                    },
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                      decoration: BoxDecoration(
                        color: isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.send_rounded, size: 14, color: ThalaivaaTheme.brandAmber),
                          const SizedBox(width: 8),
                          Expanded(child: Text(msg, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600))),
                        ],
                      ),
                    ),
                  ),
                )),
          ],
        ),
      ),
    );
  }
}

// Custom Painter for Enterprise Stylized Route Map
class _SaaSRoutePainter extends CustomPainter {
  final double progress;
  final bool isDark;
  final LiveTrackingStage stage;

  _SaaSRoutePainter({required this.progress, required this.isDark, required this.stage});

  @override
  void paint(Canvas canvas, Size size) {
    final gridPaint = Paint()
      ..color = (isDark ? Colors.white : Colors.black).withValues(alpha: 0.04)
      ..strokeWidth = 1.0;

    // Background road map grids
    for (double x = 0; x < size.width; x += 35) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), gridPaint);
    }
    for (double y = 0; y < size.height; y += 35) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), gridPaint);
    }

    // Path Curve: Branch (Left) to Customer (Right)
    final start = Offset(40, size.height * 0.52);
    final end = Offset(size.width - 40, size.height * 0.52);
    final control1 = Offset(size.width * 0.35, size.height * 0.25);
    final control2 = Offset(size.width * 0.65, size.height * 0.75);

    final path = Path()
      ..moveTo(start.dx, start.dy)
      ..cubicTo(control1.dx, control1.dy, control2.dx, control2.dy, end.dx, end.dy);

    // Inactive road base
    final roadPaint = Paint()
      ..color = (isDark ? const Color(0xFF334155) : const Color(0xFFCBD5E1))
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5.0
      ..strokeCap = StrokeCap.round;
    canvas.drawPath(path, roadPaint);

    // Active Journey Gradient Progress
    final activePaint = Paint()
      ..color = ThalaivaaTheme.brandAmber
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5.0
      ..strokeCap = StrokeCap.round;

    final pathMetrics = path.computeMetrics().toList();
    if (pathMetrics.isNotEmpty) {
      final metric = pathMetrics.first;
      final extractPath = metric.extractPath(0, metric.length * progress);
      canvas.drawPath(extractPath, activePaint);

      // Rider Marker Location along curve
      final tangent = metric.getTangentForOffset(metric.length * progress);
      if (tangent != null) {
        final riderPos = tangent.position;

        // Pulse beacon ring
        final pulsePaint = Paint()
          ..color = ThalaivaaTheme.brandAmber.withValues(alpha: 0.3)
          ..style = PaintingStyle.fill;
        canvas.drawCircle(riderPos, 16, pulsePaint);

        final markerBgPaint = Paint()
          ..color = ThalaivaaTheme.primaryDeep
          ..style = PaintingStyle.fill;
        canvas.drawCircle(riderPos, 10, markerBgPaint);

        final markerBorder = Paint()
          ..color = Colors.white
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2.5;
        canvas.drawCircle(riderPos, 10, markerBorder);
      }
    }

    // Origin Restaurant Pin
    final originPaint = Paint()..color = ThalaivaaTheme.brandAmber;
    canvas.drawCircle(start, 7, originPaint);

    // Destination Pin
    final destPaint = Paint()..color = ThalaivaaTheme.vegGreen;
    canvas.drawCircle(end, 7, destPaint);
  }

  @override
  bool shouldRepaint(covariant _SaaSRoutePainter oldDelegate) {
    return oldDelegate.progress != progress || oldDelegate.stage != stage || oldDelegate.isDark != isDark;
  }
}
"""

with open(order_screen_path, 'w', encoding='utf-8') as f:
    f.write(order_screen_content)
print("Updated order_screen.dart successfully.")
