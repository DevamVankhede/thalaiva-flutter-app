<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Str;
use App\Models\Branch;
use App\Models\Category;
use App\Models\Product;
use App\Models\ProductVariant;
use App\Models\ModifierGroup;
use App\Models\ModifierOption;
use App\Models\Coupon;
use App\Models\User;
use App\Models\Admin;
use App\Models\Order;
use App\Models\OrderItem;
use App\Models\OrderStatusLog;
use App\Models\Payment;
use App\Models\RbacRole;
use App\Models\RbacPermission;
use App\Models\RbacRolePermission;
use App\Models\AdminRbacAssignment;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // 1. Create Branches
        $cityLightBranch = Branch::firstOrCreate(
            ['slug' => 'thalaivaa-city-light'],
            [
                'name' => 'Thalaivaa - City Light (Main)',
                'address_line' => 'Shop 12-14, City Light Town, Surat, Gujarat 395007',
                'phone' => '+91 92170 02598',
                'is_active' => true,
            ]
        );

        $vesuBranch = Branch::firstOrCreate(
            ['slug' => 'thalaivaa-vesu'],
            [
                'name' => 'Thalaivaa - Vesu Branch',
                'address_line' => 'VIP Road, Vesu, Surat, Gujarat 395007',
                'phone' => '+91 92170 02599',
                'is_active' => true,
            ]
        );

        $adajanBranch = Branch::firstOrCreate(
            ['slug' => 'thalaivaa-adajan'],
            [
                'name' => 'Thalaivaa - Adajan Hub',
                'address_line' => 'L.P. Savani Road, Adajan, Surat, Gujarat 395009',
                'phone' => '+91 92170 02600',
                'is_active' => true,
            ]
        );

        $branches = [$cityLightBranch, $vesuBranch, $adajanBranch];

        // 2. Default Admin & Customer
        $admin = Admin::firstOrCreate(
            ['email' => 'admin@thalaivaa.com'],
            [
                'password_hash' => bcrypt('Admin@Thalaivaa2026'),
                'is_active' => true,
            ]
        );

        User::firstOrCreate(
            ['phone' => '+919217002598'],
            [
                'name' => 'Thalaivaa Customer',
                'email' => 'customer@thalaivaa.com',
                'password' => bcrypt('Password123!'),
                'is_active' => true,
                'otp_verified_at' => now(),
            ]
        );

        // 3. Seed RBAC Roles & Permissions
        $superAdminRole = RbacRole::firstOrCreate(
            ['name' => 'super_admin'],
            [
                'display_name' => 'Super Administrator',
                'description' => 'Full unrestricted system access across all branches.',
                
            ]
        );

        $managerRole = RbacRole::firstOrCreate(
            ['name' => 'branch_manager'],
            [
                'display_name' => 'Branch Manager',
                'description' => 'Manages branch catalog, orders, and operational staff.',
                
            ]
        );

        $kitchenRole = RbacRole::firstOrCreate(
            ['name' => 'kitchen_operator'],
            [
                'display_name' => 'Kitchen Operator',
                'description' => 'Views and updates live kitchen orders.',
                
            ]
        );

        $permissions = [
            'catalog.manage' => ['display' => 'Manage Catalog', 'module' => 'Catalog'],
            'orders.view' => ['display' => 'View Orders', 'module' => 'Orders'],
            'orders.update' => ['display' => 'Update Orders', 'module' => 'Orders'],
            'coupons.manage' => ['display' => 'Manage Coupons', 'module' => 'Promotions'],
            'settings.manage' => ['display' => 'Manage Settings', 'module' => 'Settings'],
        ];

        foreach ($permissions as $pName => $pData) {
            $perm = RbacPermission::firstOrCreate(
                ['name' => $pName],
                [
                    'description' => $pData['display'],
                    'module' => $pData['module'],
                ]
            );

            DB::table('rbac_role_permissions')->updateOrInsert([
                'role_id' => $superAdminRole->id,
                'permission_id' => $perm->id,
            ]);
        }

        AdminRbacAssignment::firstOrCreate([
            'admin_id' => $admin->id,
            'role_id' => $superAdminRole->id,
            'branch_id' => $cityLightBranch->id,
        ]);

        // 4. Coupons (Universal across all branches)
        Coupon::firstOrCreate(
            ['code' => 'THALAIVAA50'],
            [
                'branch_id' => null,
                'type' => 'fixed',
                'value' => 50,
                'valid_from' => now()->subDay(),
                'valid_to' => now()->addMonths(6),
                'max_uses' => 5000,
                'used_count' => 12,
                'is_active' => true,
            ]
        );

        Coupon::firstOrCreate(
            ['code' => 'FEAST100'],
            [
                'branch_id' => null,
                'type' => 'fixed',
                'value' => 100,
                'valid_from' => now()->subDay(),
                'valid_to' => now()->addMonths(6),
                'max_uses' => 2000,
                'used_count' => 4,
                'is_active' => true,
            ]
        );

        // 5. Seed Catalog per Branch
        $categoriesData = [
            'Morning Tiffin & Tiffin' => ['slug' => 'morning-tiffin', 'sort' => 1],
            'Dosas & Crispy Roasts' => ['slug' => 'dosas-roasts', 'sort' => 2],
            'South Indian Meals & Thali' => ['slug' => 'meals-thali', 'sort' => 3],
            'Chettinad Curries & Gravies' => ['slug' => 'curries-gravies', 'sort' => 4],
            'Breads & Rice Varieties' => ['slug' => 'breads-rice', 'sort' => 5],
            'Traditional Sweets & Desserts' => ['slug' => 'sweets-desserts', 'sort' => 6],
            'Beverages' => ['slug' => 'beverages', 'sort' => 7],
        ];

        foreach ($branches as $br) {
            $catModels = [];
            foreach ($categoriesData as $cName => $cData) {
                $catModels[$cName] = Category::firstOrCreate(
                    [
                        'branch_id' => $br->id,
                        'slug' => $cData['slug'] . '-' . $br->slug,
                    ],
                    [
                        'name' => $cName,
                        'is_active' => true,
                        'sort_order' => $cData['sort'],
                    ]
                );
            }

            // Modifier Groups
            $gheeGroup = ModifierGroup::firstOrCreate(
                [
                    'branch_id' => $br->id,
                    'name' => 'Chutney & Ghee Accompaniments',
                ],
                [
                    'modifier_type' => 'optional',
                    'min_select' => 0,
                    'max_select' => 3,
                    'is_required' => false,
                    'is_active' => true,
                ]
            );

            $mod1 = ModifierOption::firstOrCreate(
                [
                    'modifier_group_id' => $gheeGroup->id,
                    'name' => 'Extra Desi Ghee Topping',
                ],
                [
                    'price_adjustment' => 3000, // Rs 30
                    'is_available' => true,
                ]
            );

            $mod2 = ModifierOption::firstOrCreate(
                [
                    'modifier_group_id' => $gheeGroup->id,
                    'name' => 'Gunpowder Podi Spice',
                ],
                [
                    'price_adjustment' => 2500, // Rs 25
                    'is_available' => true,
                ]
            );

            $mod3 = ModifierOption::firstOrCreate(
                [
                    'modifier_group_id' => $gheeGroup->id,
                    'name' => 'Extra Coconut & Tomato Chutney Trio',
                ],
                [
                    'price_adjustment' => 2000, // Rs 20
                    'is_available' => true,
                ]
            );

            // 30 Dishes
            $dishes = [
                // Dosas
                ['cat' => 'Dosas & Crispy Roasts', 'name' => 'Ghee Roast Masala Dosa', 'slug' => 'ghee-roast-masala-dosa', 'price' => 18000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥞', 'desc' => 'Crispy golden crepe roasted in pure desi ghee with spiced potato masala.'],
                ['cat' => 'Dosas & Crispy Roasts', 'name' => 'Mysore Cheese Burst Dosa', 'slug' => 'mysore-cheese-burst-dosa', 'price' => 24000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🧀', 'desc' => 'Spicy red garlic-chutney smeared crepe with molten mozzarella.'],
                ['cat' => 'Dosas & Crispy Roasts', 'name' => 'Rava Onion Masala Dosa', 'slug' => 'rava-onion-masala-dosa', 'price' => 19000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥞', 'desc' => 'Semolina crepe laced with finely chopped shallots and roasted cashews.'],
                ['cat' => 'Dosas & Crispy Roasts', 'name' => 'Podi Ghee Karam Dosa', 'slug' => 'podi-ghee-karam-dosa', 'price' => 21000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🌶️', 'desc' => 'Crunchy crepe generously dusted with fiery Gunpowder Podi and cow ghee.'],
                ['cat' => 'Dosas & Crispy Roasts', 'name' => 'Chettinad Mushroom Dosa', 'slug' => 'chettinad-mushroom-dosa', 'price' => 23000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🍄', 'desc' => 'Stuffed with fresh button mushrooms sautéed in Chettinad stone-ground spices.'],
                ['cat' => 'Dosas & Crispy Roasts', 'name' => 'Paper Thin Plain Golden Roast', 'slug' => 'paper-thin-plain-golden-roast', 'price' => 14000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥞', 'desc' => 'Ultra-thin long golden crepe served with Madras sambar and 3 chutneys.'],

                // Morning Tiffin
                ['cat' => 'Morning Tiffin & Tiffin', 'name' => 'Steamed Button Ghee Idli (14 pcs)', 'slug' => 'steamed-button-ghee-idli', 'price' => 15000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥟', 'desc' => 'Mini melt-in-mouth button idlis submerged in hot spiced Madras sambar and ghee.'],
                ['cat' => 'Morning Tiffin & Tiffin', 'name' => 'Crispy Medu Vada (2 pcs)', 'slug' => 'crispy-medu-vada', 'price' => 12000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🍩', 'desc' => 'Crispy golden fried lentil donuts with crushed pepper, coconut chutney & sambar.'],
                ['cat' => 'Morning Tiffin & Tiffin', 'name' => 'Kanchipuram Spiced Idli (2 pcs)', 'slug' => 'kanchipuram-spiced-idli', 'price' => 16000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🥟', 'desc' => 'Temple-style steamed idlis tempered with black pepper, dry ginger, and cashews.'],
                ['cat' => 'Morning Tiffin & Tiffin', 'name' => 'Sambar Vada Submerged (2 pcs)', 'slug' => 'sambar-vada-submerged', 'price' => 14000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥣', 'desc' => 'Hot crispy medu vadas soaked in aromatic vegetable sambar and coriander.'],
                ['cat' => 'Morning Tiffin & Tiffin', 'name' => 'Ghee Podi Mini Tossed Idlis (12 pcs)', 'slug' => 'ghee-podi-mini-tossed-idlis', 'price' => 17000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🥟', 'desc' => 'Bite-sized soft idlis tossed in pan with spicy gunpowder podi and curry leaves.'],

                // Breads & Rice
                ['cat' => 'Breads & Rice Varieties', 'name' => 'Thalaivaa Special Chettinad Biryani', 'slug' => 'thalaivaa-chettinad-biryani', 'price' => 29000, 'is_veg' => false, 'is_spicy' => true, 'emoji' => '🍚', 'desc' => 'Seeraga Samba rice slow cooked with stone-ground Chettinad spices.'],
                ['cat' => 'Breads & Rice Varieties', 'name' => 'Chettinad Veggie Dum Biryani', 'slug' => 'chettinad-veggie-dum-biryani', 'price' => 24000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🍛', 'desc' => 'Seeraga samba rice cooked with garden veggies, whole spices, and salna.'],
                ['cat' => 'Breads & Rice Varieties', 'name' => 'Traditional Curd Rice with Tadka', 'slug' => 'traditional-curd-rice-tadka', 'price' => 13000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥣', 'desc' => 'Comforting creamy yogurt rice tempered with mustard, green chili, and pomegranate.'],
                ['cat' => 'Breads & Rice Varieties', 'name' => 'Bisi Bele Bath with Crisp Boondi', 'slug' => 'bisi-bele-bath-boondi', 'price' => 16000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🍲', 'desc' => 'Karnataka rice, lentils, and assorted vegetables topped with ghee and boondi.'],
                ['cat' => 'Breads & Rice Varieties', 'name' => 'Malabar Ghee Rice with Veg Kurma', 'slug' => 'malabar-ghee-rice-kurma', 'price' => 21000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🍚', 'desc' => 'Fragrant Kaima rice sauteed in ghee with cashews, served with vegetable kurma.'],

                // Curries & Meals
                ['cat' => 'Chettinad Curries & Gravies', 'name' => 'Chettinad Paneer Masala Gravy', 'slug' => 'chettinad-paneer-masala-gravy', 'price' => 26000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🥘', 'desc' => 'Cottage cheese cubes simmered in roasted peppercorn and coconut gravy.'],
                ['cat' => 'South Indian Meals & Thali', 'name' => 'South Indian Executive Meals Thali', 'slug' => 'south-indian-executive-meals-thali', 'price' => 32000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🍱', 'desc' => 'Grand feast with Rice, Sambar, Rasam, Kara Kuzhambu, Poriyal, Curd, and Sweet.'],
                ['cat' => 'Chettinad Curries & Gravies', 'name' => 'Ennai Kathirikai Curry (Baby Brinjal)', 'slug' => 'ennai-kathirikai-curry', 'price' => 22000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🍆', 'desc' => 'Tender brinjals in spicy sesame-peanut and tamarind gravy.'],
                ['cat' => 'Chettinad Curries & Gravies', 'name' => 'Malabar Vegetable Kurma with 2 Parottas', 'slug' => 'malabar-vegetable-kurma-parottas', 'price' => 24000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🫓', 'desc' => 'Layered flaky Malabar Parottas served with coconut vegetable stew.'],
                ['cat' => 'Chettinad Curries & Gravies', 'name' => 'Chettinad Mushroom Pepper Fry', 'slug' => 'chettinad-mushroom-pepper-fry', 'price' => 25000, 'is_veg' => true, 'is_spicy' => true, 'emoji' => '🍄', 'desc' => 'Semi-dry spicy preparation of mushrooms with black pepper and shallots.'],

                // Sweets & Desserts
                ['cat' => 'Traditional Sweets & Desserts', 'name' => 'Royal Elaneer Payasam (Tender Coconut)', 'slug' => 'royal-elaneer-payasam', 'price' => 14000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥥', 'desc' => 'Chilled dessert made with tender coconut pulp, condensed milk, and cardamom.'],
                ['cat' => 'Traditional Sweets & Desserts', 'name' => 'Authentic Tirunelveli Ghee Halwa', 'slug' => 'tirunelveli-ghee-halwa', 'price' => 16000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🍮', 'desc' => 'Legendary wheat milk halwa cooked for hours in pure cow ghee and palm sugar.'],
                ['cat' => 'Traditional Sweets & Desserts', 'name' => 'Pineapple Rava Kesari with Saffron', 'slug' => 'pineapple-rava-kesari-saffron', 'price' => 12000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🍍', 'desc' => 'Glistening semolina pudding flavored with fresh pineapple and Kashmiri saffron.'],
                ['cat' => 'Traditional Sweets & Desserts', 'name' => 'Mysore Pak (Melt-in-Mouth)', 'slug' => 'mysore-pak-melt-in-mouth', 'price' => 13000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🧈', 'desc' => 'Royal sweet crafted from besan gram flour, sugar, and generous desi ghee.'],
                ['cat' => 'Traditional Sweets & Desserts', 'name' => 'Crispy Sweet Malpua with Rabri (2 pcs)', 'slug' => 'sweet-malpua-rabri', 'price' => 15000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥞', 'desc' => 'Golden fried pancake soaked in cardamom syrup with thickened rabri.'],

                // Beverages
                ['cat' => 'Beverages', 'name' => 'Authentic Filter Kaapi (Degree Coffee)', 'slug' => 'authentic-filter-kaapi', 'price' => 7000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '☕', 'desc' => 'Traditional South Indian chicory-blend brew frothed with steaming milk.'],
                ['cat' => 'Beverages', 'name' => 'Madurai Famous Jigarthanda Special', 'slug' => 'madurai-jigarthanda-special', 'price' => 12000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🍨', 'desc' => 'Heart-cooling drink with almond gum, nannari syrup, basundi milk and ice cream.'],
                ['cat' => 'Beverages', 'name' => 'Spiced Butter Milk (Neer Mor)', 'slug' => 'spiced-butter-milk-neer-mor', 'price' => 5000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🥛', 'desc' => 'Refreshing churned buttermilk with ginger, green chili, and curry leaves.'],
                ['cat' => 'Beverages', 'name' => 'Fresh Sugarcane Ginger Lime Cooler', 'slug' => 'fresh-sugarcane-ginger-lime-cooler', 'price' => 6000, 'is_veg' => true, 'is_spicy' => false, 'emoji' => '🍹', 'desc' => 'Cold sugarcane juice balanced with spicy ginger and fresh lime.'],
            ];

            foreach ($dishes as $dish) {
                $cat = $catModels[$dish['cat']];
                $prod = Product::firstOrCreate(
                    [
                        'branch_id' => $br->id,
                        'slug' => $dish['slug'] . '-' . $br->slug,
                    ],
                    [
                        'category_id' => $cat->id,
                        'name' => $dish['name'],
                        'base_price' => $dish['price'],
                        'is_veg' => $dish['is_veg'],
                        'is_spicy' => $dish['is_spicy'],
                        'is_available' => true,
                        'meta_json' => [
                            'emoji' => $dish['emoji'],
                            'description' => $dish['desc'],
                            'rating' => 4.9,
                            'rating_count' => rand(120, 680),
                        ],
                    ]
                );

                ProductVariant::firstOrCreate(
                    [
                        'product_id' => $prod->id,
                        'name' => 'Regular',
                    ],
                    [
                        'sku' => strtoupper(substr($dish['slug'], 0, 4)) . '-REG',
                        'price_adjustment' => 0,
                        'is_default' => true,
                        'is_available' => true,
                    ]
                );

                DB::table('product_modifier_links')->updateOrInsert(
                    [
                        'product_id' => $prod->id,
                        'modifier_group_id' => $gheeGroup->id,
                    ],
                    [
                        'is_required' => false,
                    ]
                );
            }
        }

        // 6. Test Users for Multi-User Authentication & Order History
        // User A: Multiple Orders
        $userA = User::firstOrCreate(
            ['email' => 'usera@test.com'],
            [
                'phone' => '+919800000001',
                'name' => 'Aarav Sharma',
                'password' => bcrypt('Password123!'),
                'is_active' => true,
                'otp_verified_at' => now(),
            ]
        );

        // User B: Single Order
        $userB = User::firstOrCreate(
            ['email' => 'userb@test.com'],
            [
                'phone' => '+919800000002',
                'name' => 'Bhavna Patel',
                'password' => bcrypt('Password123!'),
                'is_active' => true,
                'otp_verified_at' => now(),
            ]
        );

        // User C: Zero Orders
        $userC = User::firstOrCreate(
            ['email' => 'userc@test.com'],
            [
                'phone' => '+919800000003',
                'name' => 'Chirag Mehta',
                'password' => bcrypt('Password123!'),
                'is_active' => true,
                'otp_verified_at' => now(),
            ]
        );

        $dosaProduct = Product::where('slug', 'ghee-roast-masala-dosa-' . $cityLightBranch->slug)->first() ?? Product::first();
        $mysoreDosa = Product::where('slug', 'mysore-cheese-burst-dosa-' . $cityLightBranch->slug)->first() ?? Product::first();
        $kaapiProduct = Product::where('slug', 'authentic-filter-kaapi-' . $cityLightBranch->slug)->first() ?? Product::first();
        $biryaniProduct = Product::where('slug', 'chettinad-veggie-dum-biryani-' . $vesuBranch->slug)->first() ?? Product::first();

        // Seed Orders for User A (3 Orders)
        if (Order::where('user_id', $userA->id)->count() === 0) {
            // User A Order 1: ORD-001 (Delivered)
            $orderA1 = Order::create([
                'user_id' => $userA->id,
                'branch_id' => $cityLightBranch->id,
                'order_number' => 'ORD-001',
                'status' => 'delivered',
                'payment_status' => 'paid',
                'subtotal' => 36000,
                'tax_amount' => 1800,
                'discount_amount' => 5000,
                'delivery_charge' => 4000,
                'total_amount' => 36800,
                'discount_type' => 'fixed',
                'discount_value' => 50.00,
                'delivery_name' => $userA->name,
                'delivery_phone' => $userA->phone,
                'delivery_address_line' => 'Flat 402, Royal Palms, City Light',
                'delivery_city' => 'Surat',
                'delivery_postal' => '395007',
                'status_changed_at' => now()->subHours(2),
                'created_at' => now()->subDays(2),
            ]);

            OrderItem::create([
                'order_id' => $orderA1->id,
                'product_id' => $dosaProduct->id,
                'variant_id' => $dosaProduct->variants->first()?->id,
                'quantity' => 2,
                'unit_price' => 18000,
                'line_total' => 36000,
                'product_name_snapshot' => $dosaProduct->name,
                'variant_name_snapshot' => 'Regular',
            ]);

            OrderStatusLog::create([
                'order_id' => $orderA1->id,
                'from_status' => 'out_for_delivery',
                'to_status' => 'delivered',
                'actor_type' => 'driver',
                'notes' => 'Handed over at doorstep',
                'created_at' => now()->subHours(2),
            ]);

            // User A Order 2: ORD-002 (Preparing)
            $orderA2 = Order::create([
                'user_id' => $userA->id,
                'branch_id' => $cityLightBranch->id,
                'order_number' => 'ORD-002',
                'status' => 'preparing',
                'payment_status' => 'paid',
                'subtotal' => 24000,
                'tax_amount' => 1200,
                'discount_amount' => 0,
                'delivery_charge' => 4000,
                'total_amount' => 29200,
                'delivery_name' => $userA->name,
                'delivery_phone' => $userA->phone,
                'delivery_address_line' => 'Flat 402, Royal Palms, City Light',
                'delivery_city' => 'Surat',
                'delivery_postal' => '395007',
                'status_changed_at' => now()->subMinutes(15),
                'created_at' => now()->subMinutes(20),
            ]);

            OrderItem::create([
                'order_id' => $orderA2->id,
                'product_id' => $mysoreDosa->id,
                'variant_id' => $mysoreDosa->variants->first()?->id,
                'quantity' => 1,
                'unit_price' => 24000,
                'line_total' => 24000,
                'product_name_snapshot' => $mysoreDosa->name,
                'variant_name_snapshot' => 'Regular',
            ]);

            OrderStatusLog::create([
                'order_id' => $orderA2->id,
                'from_status' => 'confirmed',
                'to_status' => 'preparing',
                'actor_type' => 'kds',
                'notes' => 'Chef roasting dosa',
                'created_at' => now()->subMinutes(15),
            ]);

            // User A Order 3: ORD-003 (Confirmed)
            $orderA3 = Order::create([
                'user_id' => $userA->id,
                'branch_id' => $cityLightBranch->id,
                'order_number' => 'ORD-003',
                'status' => 'confirmed',
                'payment_status' => 'paid',
                'subtotal' => 14000,
                'tax_amount' => 700,
                'discount_amount' => 0,
                'delivery_charge' => 4000,
                'total_amount' => 18700,
                'delivery_name' => $userA->name,
                'delivery_phone' => $userA->phone,
                'delivery_address_line' => 'Flat 402, Royal Palms, City Light',
                'delivery_city' => 'Surat',
                'delivery_postal' => '395007',
                'status_changed_at' => now()->subMinutes(5),
                'created_at' => now()->subMinutes(5),
            ]);

            OrderItem::create([
                'order_id' => $orderA3->id,
                'product_id' => $kaapiProduct->id,
                'variant_id' => $kaapiProduct->variants->first()?->id,
                'quantity' => 2,
                'unit_price' => 7000,
                'line_total' => 14000,
                'product_name_snapshot' => $kaapiProduct->name,
                'variant_name_snapshot' => 'Regular',
            ]);
        }

        // Seed Orders for User B (1 Order: ORD-004)
        if (Order::where('user_id', $userB->id)->count() === 0) {
            $orderB1 = Order::create([
                'user_id' => $userB->id,
                'branch_id' => $vesuBranch->id,
                'order_number' => 'ORD-004',
                'status' => 'out_for_delivery',
                'payment_status' => 'paid',
                'subtotal' => 48000,
                'tax_amount' => 2400,
                'discount_amount' => 10000,
                'delivery_charge' => 0,
                'total_amount' => 40400,
                'discount_type' => 'fixed',
                'discount_value' => 100.00,
                'delivery_name' => $userB->name,
                'delivery_phone' => $userB->phone,
                'delivery_address_line' => '102 Green Acres, VIP Road, Vesu',
                'delivery_city' => 'Surat',
                'delivery_postal' => '395007',
                'status_changed_at' => now()->subMinutes(10),
                'created_at' => now()->subMinutes(40),
            ]);

            OrderItem::create([
                'order_id' => $orderB1->id,
                'product_id' => $biryaniProduct->id,
                'variant_id' => $biryaniProduct->variants->first()?->id,
                'quantity' => 2,
                'unit_price' => 24000,
                'line_total' => 48000,
                'product_name_snapshot' => $biryaniProduct->name,
                'variant_name_snapshot' => 'Regular',
            ]);

            OrderStatusLog::create([
                'order_id' => $orderB1->id,
                'from_status' => 'preparing',
                'to_status' => 'out_for_delivery',
                'actor_type' => 'driver',
                'notes' => 'Rider dispatched on EV',
                'created_at' => now()->subMinutes(10),
            ]);
        }
    }
}
