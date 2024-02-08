from django.shortcuts import render, redirect
import requests
from django.conf import settings
from django.contrib import messages
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from .models import User, CryptoUser, Wallet, Kyc
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from .models import Transaction, CryptoCurrency
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction

# Create your views here.

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
parameters = {"start": "1", "limit": "5000"}
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "677c00f0-20b4-45f1-8642-cca4e2d9154c",
}

session = Session()
session.headers.update(headers)


def index(request):
    return render(request, "index.html")


def home(request):
    try:
        return render(request, "home.html")

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def dashboard(request):
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        # Check if 'data' key exists in the dictionary
        apidata = data.get("data", [])

        selected_coin_details = None

        # Check if a coin is selected
        search_input = request.GET.get("searchInput")
        if search_input:
            # Find the selected coin in apidata
            selected_coin_details = next(
                (
                    coin
                    for coin in apidata
                    if coin["name"].lower() == search_input.lower()
                ),
                None,
            )
            # Filter apidata based on the search input
            apidata = [
                coin for coin in apidata if coin["name"].lower() == search_input.lower()
            ]

        # Check if 'show_coin_list' parameter is present and set to 'true'
        show_coin_list = request.GET.get("show_coin_list") == "true"

        return render(
            request,
            "dashboard.html",
            {
                "apidata": apidata,
                "selected_coin_details": selected_coin_details,
                "show_coin_list": show_coin_list,
            },
        )

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        mobilenumber = request.POST.get("mobilenumber")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("/signup/")
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            email=email,
            username=username,
            password=password1,
        )

        cryptouser = CryptoUser.objects.create(user=user, mobilenumber=mobilenumber)
        print(cryptouser)

        Wallet.objects.create(walletuser=user, balance=0)
        user.save()

        return redirect("/signin/")

    return render(request, "sign-up.html")


def signin(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = User.objects.get(username=username)

            if not CryptoUser.objects.filter(user_id=user.id).exists():
                messages.error(request, "Invalid username or password")
                return redirect("/signin/")

            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Invalid username or password")
            else:
                login(request, user)
                return redirect("/profile/")

    except User.DoesNotExist:
        # Handle the case where the user does not exist
        messages.error(request, "Invalid username or password")
        return redirect("/signin/")
    except Exception as e:
        # Log the exception or handle it as needed
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/signin/")
    return render(request, "sign-in.html")


def userlogout(request):
    logout(request)
    return redirect("/")


def afterloginpage(request):
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        apidata = data["data"]
        selected_coin_details = None

        # Check if a coin is selected
        search_input = request.GET.get("searchInput")
        if search_input:
            # Find the selected coin in apidata
            selected_coin_details = next(
                (
                    coin
                    for coin in apidata
                    if coin["name"].lower() == search_input.lower()
                ),
                None,
            )
            # Filter apidata based on the search input
            apidata = [
                coin for coin in apidata if coin["name"].lower() == search_input.lower()
            ]

        # Check if 'show_coin_list' parameter is present and set to 'true'
        show_coin_list = request.GET.get("show_coin_list") == "true"

        return render(
            request,
            "profile.html",
            {
                "apidata": apidata,
                "selected_coin_details": selected_coin_details,
                "show_coin_list": show_coin_list,
            },
        )

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def kyc(request):
    user = request.user
    print(user)
    if request.method == "POST":
        documenttype = request.POST.get("documenttype")
        documentnumber = request.POST.get("documentnumber")
        dateofbirth = request.POST.get("dateofbirth")
        address = request.POST.get("address")
        documentimage = request.FILES.get("documentimage")
        print(address, documenttype, documentnumber, dateofbirth, documentimage)

        is_kyc = Kyc.objects.create(
            user=user,
            documenttype=documenttype,
            documentnumber=documentnumber,
            dateofbirth=dateofbirth,
            address=address,
            documentimage=documentimage,
            verified_user=False,
        )
        if is_kyc is not None:
            user = CryptoUser.objects.get(user=user)
            user.is_kyc_done = True
            user.save()

        return redirect("/")
    return render(request, "kyc.html")


def userprofile(request):
    # Assuming user is authenticated, you can add appropriate authentication checks
    user = request.user

    # Fetch user's transactions
    user_transactions = Transaction.objects.filter(user=user)
    print(user_transactions)
    # Pass user and transactions to the template
    return render(
        request,
        "userprofile.html",
        {"user": user, "user_transactions": user_transactions},
    )


def buy_view(request, symbol):
    # Check if the request method is GET
    if request.method == "GET":
        # Assuming that the user is logged in
        user = request.user

        # Get the quantity from the URL parameter
        quantity = request.GET.get("quantity")
        print(quantity)

        # Check if the quantity is provided and is a valid number
        if quantity is not None:
            try:
                quantity = Decimal(quantity)
            except ValueError:
                messages.error(request, "Invalid quantity")
                return redirect("/profile")

            if quantity <= 0:
                messages.error(request, "Quantity must be greater than zero")
                return redirect("profile")

            # Get the selected coin details dynamically
            selected_coin_details = get_selected_coin_details(symbol)

            if not selected_coin_details:
                messages.error(request, "Failed to fetch coin details")
                return redirect("profile")

            # Get the user's wallet or create one if not exists
            wallet, created = Wallet.objects.get_or_create(walletuser=user)

            # Convert the current price to Decimal
            current_price = Decimal(str(selected_coin_details["current_price"]))
            print(current_price)
            # Calculate the total cost based on the coin's current price
            total_cost = current_price * quantity
            print(total_cost)
            wallet_instance, created = Wallet.objects.get_or_create(walletuser=user)

            # ...

            # Check if the user has enough balance
            if wallet_instance.balance >= total_cost:
                # Update the user's balance
                wallet_instance.balance -= total_cost
                wallet_instance.save()

                # Get or create a CryptoCurrency instance
                crypto_currency, created = CryptoCurrency.objects.get_or_create(
                    symbol=selected_coin_details["symbol"],
                    defaults={
                        "name": selected_coin_details["name"],
                        "current_price": current_price,
                        "percent_change_24h": selected_coin_details[
                            "percent_change_24h"
                        ],
                    },
                )

                # Set the buy_price based on the current price
                buy_price = selected_coin_details["current_price"]

                # Create a new transaction
                Transaction.objects.create(
                    user=user,
                    coin=crypto_currency,
                    amount=quantity,
                    buy_price=buy_price,
                    total_cost=total_cost,  # Set the total_cost
                    timestamp=timezone.now(),  # Import timezone from django.utils
                )

                messages.success(request, f"Successfully bought {quantity} {symbol}!")
                return redirect("/userprofile/")
            else:
                messages.error(request, "Insufficient balance")

    return redirect("/userprofile/")


def get_selected_coin_details(symbol):
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {"start": "1", "limit": "5000", "convert": "USD"}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "677c00f0-20b4-45f1-8642-cca4e2d9154c",
        }

        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()

        # Check if 'data' key exists in the dictionary
        apidata = data.get("data", [])

        # Find the selected coin in apidata
        selected_coin_details = next(
            (coin for coin in apidata if coin["symbol"].lower() == symbol.lower()),
            None,
        )

        if selected_coin_details:
            # Convert the selected coin details to a dictionary
            current_price_str = selected_coin_details["quote"]["USD"]["price"]
            current_price = Decimal(current_price_str)

            return {
                "name": selected_coin_details["name"],
                "symbol": selected_coin_details["symbol"],
                "image_url": f"https://coinicons-api.vercel.app/api/icon/{selected_coin_details['symbol'].lower()}",
                "current_price": current_price,
                "percent_change_24h": selected_coin_details["quote"]["USD"][
                    "percent_change_24h"
                ],
            }
        else:
            return None

    except Exception as e:
        # Handle the exception as needed
        print(f"An error occurred: {str(e)}")
        return None


def sell_coin(request):
    if request.method == "POST":
        user = request.user
        coin_symbol = request.POST.get("coin_symbol")
        quantity = request.POST.get("quantity")

        try:
            # Retrieve the user's transactions for the specified coin
            transactions = user.transactions.filter(coin__symbol=coin_symbol)
            if not transactions.exists():
                return JsonResponse(
                    {"error": f"You do not own any {coin_symbol} to sell."}, status=400
                )

            # Check if the quantity is provided and is a valid number
            if quantity is not None:
                try:
                    quantity = Decimal(quantity)
                    if quantity <= 0:
                        raise ValueError("Quantity must be greater than zero")
                except ValueError:
                    return JsonResponse({"error": "Invalid quantity."}, status=400)
            else:
                return JsonResponse({"error": "Quantity is required."}, status=400)

            # Calculate the total amount in USD based on the current market price
            total_sale_amount = sum(
                transaction.coin.current_price * transaction.amount
                for transaction in transactions
            )

            # Check if the user has a wallet and if the balance is sufficient
            with db_transaction.atomic():
                try:
                    wallet = user.wallet
                    if wallet.balance < total_sale_amount:
                        return JsonResponse(
                            {"error": "Insufficient wallet balance."}, status=400
                        )
                except Wallet.DoesNotExist:
                    return JsonResponse(
                        {"error": "User does not have a wallet."}, status=400
                    )

                # Update the user's wallet balance
                wallet.balance += total_sale_amount
                wallet.save()

                # Handle deletion of transactions based on the provided quantity
                remaining_quantity = quantity

                for transaction in transactions:
                    if remaining_quantity >= transaction.amount:
                        # If selling all quantity, delete the transaction
                        transaction.delete()
                    else:
                        # If selling part of the quantity, update the transaction amount
                        transaction.amount -= remaining_quantity
                        transaction.save()

                    remaining_quantity -= transaction.amount
                    if remaining_quantity <= 0:
                        break

            messages.success(request, f"Successfully sold {quantity} {coin_symbol}!")
            return redirect("/userprofile/")  # Adjust the URL as needed

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request."}, status=400)


def get_live_prices(request):
    # Fetch live prices from the database
    live_prices = CryptoCurrency.objects.values(
        "symbol", "current_price", "profit_loss_percent"
    )

    return JsonResponse(list(live_prices), safe=False)
