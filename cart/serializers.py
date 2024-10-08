from rest_framework import serializers
from .models import Cart, CartItem
from shop.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'price']
        


    def add_item(self, validated_data):
        cart = validated_data.get('cart')
        product = validated_data.get('product')
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price': product.price, 'quantity': validated_data.get('quantity')}
        )

        if not created:
            cart_item.quantity += validated_data('quantity', 1)
            cart_item.save()
            cart_item.cart.calculate_total_price()
        cart.calculate_total_price()


    
    def remove_item(self, validated_data):
        cart = validated_data.get('cart')
        quantity = validated_data.get('quantity')
        product = validated_data.get('product')

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()
                cart_item.cart.calculate_total_price()
            cart_item.delete()
        except:       
            cart_item.DoesNotExist
            raise serializers.ValidationError('cart item does not exist.')
                
        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='item', read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'created_at', 'total_amount', 'cart_key', 'items']
        read_only_fiels = ['user']


    def total_amount(self, obj):
        return obj.calculate_total_price()


    def create(self, validated_data):
        user = validated_data.get('user')
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart
    

    def destroy(self, validated_data):
        user = validated_data.get('user')
        cart = Cart.objects.get(user=user)
        if cart:
            cart.delete()
        serializers.ValidationError('cart does not exist.')   
        

    


        