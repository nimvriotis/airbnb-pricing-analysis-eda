import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# General settings
sns.set_style("whitegrid")
pd.set_option("display.max_columns", None)


def load_city_data():
    city_files = {
        "Amsterdam": ["data/amsterdam_weekdays.csv", "data/amsterdam_weekends.csv"],
        "Athens": ["data/athens_weekdays.csv", "data/athens_weekends.csv"],
        "Barcelona": ["data/barcelona_weekdays.csv", "data/barcelona_weekends.csv"],
        "Berlin": ["data/berlin_weekdays.csv", "data/berlin_weekends.csv"],
        "Budapest": ["data/budapest_weekdays.csv", "data/budapest_weekends.csv"],
        "Lisbon": ["data/lisbon_weekdays.csv", "data/lisbon_weekends.csv"],
        "London": ["data/london_weekdays.csv", "data/london_weekends.csv"],
        "Paris": ["data/paris_weekdays.csv", "data/paris_weekends.csv"],
        "Rome": ["data/rome_weekdays.csv", "data/rome_weekends.csv"],
        "Vienna": ["data/vienna_weekdays.csv", "data/vienna_weekends.csv"],
    }

    dataframes = []

    for city, files in city_files.items():
        weekday_file, weekend_file = files

        df_weekday = pd.read_csv(weekday_file)
        df_weekday["city"] = city
        df_weekday["day_type"] = "Weekday"

        df_weekend = pd.read_csv(weekend_file)
        df_weekend["city"] = city
        df_weekend["day_type"] = "Weekend"

        dataframes.append(df_weekday)
        dataframes.append(df_weekend)

    return pd.concat(dataframes, ignore_index=True)


def clean_data(df):
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df = df.rename(columns={"realSum": "price"})

    return df


def initial_exploration(df):
    print("\nDataset shape:")
    print(df.shape)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset info:")
    print(df.info())

    print("\nDescriptive statistics:")
    print(df.describe())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nNull values:")
    print(df.isnull().sum())

    print("\nListings by city:")
    print(df["city"].value_counts())

    print("\nRoom type distribution:")
    print(df["room_type"].value_counts())

    print("\nDay type distribution:")
    print(df["day_type"].value_counts())

    print("\nSuperhost distribution:")
    print(df["host_is_superhost"].value_counts())


def create_filtered_dataset(df):
    price_limit = df["price"].quantile(0.99)
    print("\n99th percentile price limit:")
    print(price_limit)

    df_filtered = df[df["price"] <= price_limit].copy()
    return df_filtered


def plot_price_distribution_all(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["price"], bins=50)
    plt.title("Distribution of Airbnb Listing Prices")
    plt.xlabel("Price")
    plt.ylabel("Count")
    plt.savefig("images/price_distribution_including_outliers.png", bbox_inches="tight")
    plt.close()


def plot_price_distribution_filtered(df_filtered):
    plt.figure(figsize=(10, 6))
    sns.histplot(df_filtered["price"], bins=50)
    plt.title("Price Distribution (Filtered at 99th Percentile)")
    plt.xlabel("Price")
    plt.ylabel("Count")
    plt.savefig("images/price_distribution.png", bbox_inches="tight")
    plt.close()


def plot_avg_price_by_city(df_filtered):
    city_price = df_filtered.groupby("city")["price"].mean().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=city_price.values, y=city_price.index)
    plt.title("Average Airbnb Price by City")
    plt.xlabel("Average Price")
    plt.ylabel("City")
    plt.savefig("images/avg_price_by_city.png", bbox_inches="tight")
    plt.close()


def plot_price_by_room_type(df_filtered):
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df_filtered, x="room_type", y="price")
    plt.title("Price Distribution by Room Type")
    plt.xlabel("Room Type")
    plt.ylabel("Price")
    plt.savefig("images/price_distribution_by_room_type.png", bbox_inches="tight")
    plt.close()


def plot_price_vs_guest_capacity(df_filtered):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_filtered, x="person_capacity", y="price", alpha=0.3)
    plt.title("Price vs Guest Capacity (Scatterplot)")
    plt.xlabel("Guest Capacity")
    plt.ylabel("Price")
    plt.savefig("images/price_vs_guest_capacity_scatterplot.png", bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df_filtered, x="person_capacity", y="price")
    plt.title("Price vs Guest Capacity (Boxplot)")
    plt.xlabel("Guest Capacity")
    plt.ylabel("Price")
    plt.savefig("images/price_vs_guest_capacity_boxplot.png", bbox_inches="tight")
    plt.close()


def plot_price_vs_location(df_filtered):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df_filtered,
        x="dist",
        y="price",
        hue="metro_dist",
        palette="viridis",
        alpha=0.6
    )
    plt.title("Price vs Distance from City Center (colored by Metro Distance)")
    plt.xlabel("Distance from City Center")
    plt.ylabel("Price")
    plt.savefig("images/price_vs_city_center_dist_vs_metro_dist.png", bbox_inches="tight")
    plt.close()


def plot_superhost_price(df_filtered):
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df_filtered, x="host_is_superhost", y="price")
    plt.title("Price by Superhost Status")
    plt.xlabel("Host is Superhost")
    plt.ylabel("Price")
    plt.savefig("images/host_is_superhost.png", bbox_inches="tight")
    plt.close()


def plot_price_distribution_by_city(df_filtered):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_filtered, x="city", y="price", showfliers=False)
    plt.title("Price Distribution by City (Outliers Removed)")
    plt.xlabel("City")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.savefig("images/price_distribution_by_city.png", bbox_inches="tight")
    plt.close()


def plot_weekday_vs_weekend(df_filtered):
    city_order = (
        df_filtered[df_filtered["day_type"] == "Weekend"]
        .groupby("city")["price"]
        .mean()
        .sort_values(ascending=False)
        .index
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df_filtered,
        x="city",
        y="price",
        hue="day_type",
        order=city_order
    )
    plt.title("Average Price by City: Weekday vs Weekend")
    plt.xticks(rotation=45)
    plt.savefig("images/avg_price_by_city_weekday_vs_weekend.png", bbox_inches="tight")
    plt.close()


def plot_correlation_heatmap(df_filtered):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_filtered.corr(numeric_only=True), annot=False, cmap="YlOrRd")
    plt.title("Correlation Heatmap")
    plt.savefig("images/correlation_map.png", bbox_inches="tight")
    plt.close()


def main():
    print("Loading datasets...")
    df = load_city_data()

    print("Cleaning data...")
    df = clean_data(df)

    print("Running initial exploration...")
    initial_exploration(df)

    print("Filtering extreme price outliers for visualizations...")
    df_filtered = create_filtered_dataset(df)

    print("Creating charts...")
    plot_price_distribution_all(df)
    plot_price_distribution_filtered(df_filtered)
    plot_avg_price_by_city(df_filtered)
    plot_price_by_room_type(df_filtered)
    plot_price_vs_guest_capacity(df_filtered)
    plot_price_vs_location(df_filtered)
    plot_superhost_price(df_filtered)
    plot_price_distribution_by_city(df_filtered)
    plot_weekday_vs_weekend(df_filtered)
    plot_correlation_heatmap(df_filtered)

    print("\nAnalysis complete. All visualizations saved in the images folder.")


if __name__ == "__main__":
    main()
