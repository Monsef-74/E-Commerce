
import pandas as pd
from django.db.models import Sum
from product.models import Product
from order.models import OrderItem

def get_initial_recommendations_from_db():
    order_items_data = OrderItem.objects.select_related('product').values(
        'product__id',        
        'product__name',       
        'product__category',   
        'quantity'           
    )

    print("Raw order_items_data from ORM:", list(order_items_data)[:5])

    order_items_df = pd.DataFrame(list(order_items_data))

    print("DataFrame columns BEFORE renaming:", order_items_df.columns.tolist())
    print("DataFrame head BEFORE renaming:\n", order_items_df.head())

    order_items_df.rename(columns={
        'product__id': 'product_id',
        'product__name': 'name_y',
        'product__category': 'category'
    }, inplace=True)
    
    print("DataFrame columns AFTER renaming:", order_items_df.columns.tolist())
    print("DataFrame head AFTER renaming:\n", order_items_df.head())

    if not order_items_df.empty:
  
        if 'product_id' in order_items_df.columns:
            order_items_df['product_id'] = order_items_df['product_id'].astype(str)
        else:
            print("Error: 'product_id' column not found after renaming. Check data or renaming logic.")
            return pd.DataFrame(columns=['product_id', 'name', 'category'])
    else:
        print("DataFrame is empty after fetching data, returning empty recommendations.")
        return pd.DataFrame(columns=['product_id', 'name', 'category'])

    if order_items_df.empty:
        return pd.DataFrame(columns=['product_id', 'name', 'category'])

    sales_per_product = order_items_df.groupby(['product_id', 'name_y', 'category'])['quantity'].sum().reset_index()

    top_men = sales_per_product[sales_per_product['category'].str.lower() == 'men'] \
                        .sort_values(by='quantity', ascending=False) \
                        .head(3)[['product_id', 'name_y', 'category']]

    top_women = sales_per_product[sales_per_product['category'].str.lower() == 'women'] \
                          .sort_values(by='quantity', ascending=False) \
                          .head(3)[['product_id', 'name_y', 'category']]

    top_kids = sales_per_product[sales_per_product['category'].str.lower() == 'kids'] \
                         .sort_values(by='quantity', ascending=False) \
                         .head(2)[['product_id', 'name_y', 'category']]

 
    recommendations = pd.concat([top_men, top_women, top_kids], ignore_index=True)
    recommendations.rename(columns={'name_y': 'name'}, inplace=True)
    recommendations.reset_index(drop=True, inplace=True)
    
    return recommendations