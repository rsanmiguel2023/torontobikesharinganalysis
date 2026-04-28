import os
import matplotlib.pyplot as plt


def plot_user_type_stacked_counts(result: dict, output_path: str = "output/us07_user_type_stacked.png"):
    """
    Plot a stacked bar chart for user type counts using the US07 result dict.
    result should be:
      {
        "counts": {"Subscriber": X, "Customer": Y, "Unknown": Z},
        "avg_duration": {...}
      }
    """

    counts = result["counts"]

    # Make sure keys exist
    subscriber_count = counts.get("Subscriber", 0)
    customer_count = counts.get("Customer", 0)
    unknown_count = counts.get("Unknown", 0)

    # Single x position (one bar) called "User Types"
    x_labels = ["User Types"]
    x_pos = [0]

    # First layer: Subscriber
    plt.figure()
    plt.bar(x_pos, [subscriber_count], label="Subscriber")

    # Second layer: Customer stacked on top
    plt.bar(
        x_pos,
        [customer_count],
        bottom=[subscriber_count],
        label="Customer",
    )

    # Third layer: Unknown stacked on top of both
    plt.bar(
        x_pos,
        [unknown_count],
        bottom=[subscriber_count + customer_count],
        label="Unknown",
    )

    plt.xticks(x_pos, x_labels)
    plt.ylabel("Number of Trips")
    plt.title("US07 - User Type Breakdown (Stacked Counts)")
    plt.legend()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
