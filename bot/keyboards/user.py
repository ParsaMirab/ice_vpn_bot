from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.models import Order, Plan, Service
from bot.services.order_service import OrderService


class UserCallback:
    buy_service = "user:buy_service"
    my_services = "user:my_services"
    back_to_main = "user:back_to_main"
    register_order = "user:order:register"
    enter_discount = "user:order:discount"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="خرید سرویس", callback_data=UserCallback.buy_service, style="success"))
    builder.row(
        InlineKeyboardButton(text="سفارش‌های من", callback_data=UserCallback.my_services, style="danger"),
        InlineKeyboardButton(text="پشتیبانی", url="tg://resolve?domain=Saeedrlh", style="primary"),
    )
    return builder.as_markup()


def user_services_keyboard(services: list[Service]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for service in services:
        builder.row(
            InlineKeyboardButton(
                text=service.name,
                callback_data=f"user:buy:service:{service.id}",
                style="primary",
            )
        )
    builder.row(InlineKeyboardButton(text="بازگشت", callback_data=UserCallback.back_to_main, style="danger"))
    return builder.as_markup()


def user_plans_keyboard(service_id: int, plans: list[Plan]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for plan in plans:
        builder.row(
            InlineKeyboardButton(
                text=plan.name,
                callback_data=f"user:buy:plan:{service_id}:{plan.id}",
                style="primary",
            )
        )
    builder.row(InlineKeyboardButton(text="بازگشت", callback_data=UserCallback.buy_service, style="danger"))
    return builder.as_markup()


def plan_details_keyboard(service_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="ثبت سفارش", callback_data=UserCallback.register_order, style="success"))
    builder.row(InlineKeyboardButton(text="کد تخفیف", callback_data=UserCallback.enter_discount, style="primary"))
    builder.row(InlineKeyboardButton(text="بازگشت", callback_data=f"user:buy:service:{service_id}", style="danger"))
    return builder.as_markup()


def user_orders_keyboard(orders: list[Order]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.row(
            InlineKeyboardButton(
                text=f"#{order.id} | {OrderService.status_label(order.status)}",
                callback_data=f"user:orders:view:{order.id}",
                style=_order_status_style(order.status),
            )
        )
    builder.row(InlineKeyboardButton(text="بازگشت", callback_data=UserCallback.back_to_main, style="danger"))
    return builder.as_markup()


def user_order_details_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="بازگشت", callback_data=UserCallback.my_services, style="danger"))
    return builder.as_markup()


def _order_status_style(status: str) -> str | None:
    styles = {
        OrderService.pending: "primary",
        OrderService.approved: "success",
        OrderService.rejected: "danger",
    }
    return styles.get(status)
