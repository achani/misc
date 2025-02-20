import pandas as pd

def process_products_and_customers(products, customers, lookup_list):
    # Merge products and customers on 'product_id' with a left join to keep all products
    merged_df = pd.merge(products, customers, on='product_id', how='left')
    
    # Determine if each product is used by checking for nulls in customer_id after the merge
    merged_df['is_used'] = merged_df['customer_id'].notna()
    
    # Aggregate customer_ids by product_id, separating them with '|'
    aggregated = merged_df.groupby('product_id').agg({
        'customer_id': lambda x: '|'.join(sorted(set(x.dropna().astype(str))))
    }).rename(columns={'customer_id': 'used_by'})
    
    # Merge the aggregated data back to the products dataframe to include all products
    final_df = pd.merge(products, aggregated, on='product_id', how='left')
    
    # Fill missing values in 'used_by' with an empty string where no customers are linked
    final_df['used_by'].fillna('', inplace=True)
    final_df['is_used'] = final_df['is_used'].fillna(False)

    # Adjust 'is_used' based on 'used_by' values being entirely in 'lookup_list'
    def adjust_is_used(row):
        if row['used_by'] == '':
            return False
        customer_ids = set(row['used_by'].split('|'))
        return not customer_ids.issubset(set(lookup_list))
    
    final_df['is_used'] = final_df.apply(adjust_is_used, axis=1)
    
    # Calculate the sum of prices where 'is_used' is False
    sum_prices = final_df[final_df['is_used'] == False]['price'].sum()
    
    return final_df, sum_prices

# Example DataFrames
products = pd.DataFrame({
    'product_id': [1, 2, 3, 4],
    'price': [20.5, 15.0, 30.0, 22.5]
})

customers = pd.DataFrame({
    'product_id': [1, 2, 1, 3, 3],
    'customer_id': [101, 102, 103, 104, 105]
})

# Lookup list containing customer IDs
lookup_list = [101, 102, 104, 105]

# Process the data
result_df, sum_prices = process_products_and_customers(products, customers, lookup_list)
print(result_df)
print("Sum of prices for unused products:", sum_prices)
