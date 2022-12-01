
from .models import PerfumeBottle, CartProduct
from rest_framework.response import Response
from .serializer import CartSerializer
from rest_framework import status


def add_item_to_cart(product_id, quantity, user_cart):

    if product_id is not None and quantity is not None:
        perfumes = PerfumeBottle.objects.filter(id=product_id)
        if len(perfumes) > 0:
            perfume = perfumes[0]
        else:
            return Response({"error:": "There is no product with such id"})
        cart_products = CartProduct.objects.filter(
            product=perfume, cart=user_cart)
        if len(cart_products) > 0:
            cart_product = cart_products[0]
        else:
            cart_product = CartProduct.objects.create(
                cart=user_cart, product=perfume, quantity=0)

        if int(quantity) + cart_product.quantity <= perfume.quantity:
            cart_product.quantity = cart_product.quantity + int(quantity)
            cart_product.save()
            serializer = CartSerializer(user_cart, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "There is not enough of this product"})
    else:
        return Response({"error": "product_id or quantity has not been provided!"})


def delete_cart_item(quantity, product_id, user_cart):
    if quantity is None and product_id is None:
        CartProduct.objects.filter(cart=user_cart).delete()
        return Response({"result": "Cart has been reset"}, status=status.HTTP_200_OK)
    elif product_id is not None and quantity is None:
        perfumes = PerfumeBottle.objects.filter(id=product_id)
        if len(perfumes) > 0:
            perfume = perfumes[0]
        else:
            return Response({"error:": "There is no product with such id"}, status=status.HTTP_404_NOT_FOUND)
        CartProduct.objects.filter(
            cart=user_cart, product=perfume).delete()

    elif product_id is not None and quantity is not None:
        perfumes = PerfumeBottle.objects.filter(id=product_id)
        if len(perfumes) > 0:
            perfume = perfumes[0]
        else:
            return Response({"error:": "There is no product with such id"}, status=status.HTTP_404_NOT_FOUND)
        cartProducts = CartProduct.objects.filter(
            cart=user_cart, product=perfume)

        if len(cartProducts) > 0:
            cartProduct = cartProducts[0]
        else:
            return Response({"error:": "This product is not in the cart"}, status=status.HTTP_404_NOT_FOUND)
        if cartProduct.quantity - int(quantity) > 0:
            cartProduct.quantity = cartProduct.quantity - int(quantity)
            cartProduct.save()
        else:
            cartProduct.delete()

    serializer = CartSerializer(user_cart, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
