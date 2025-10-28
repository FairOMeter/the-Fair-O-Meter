if __name__ == "__main__":
    from plotly_template_initializer import initialize_plotly_template
    initialize_plotly_template()

    # Plotters

    from plotter_animated_pie import export_animated_pie_html
    export_animated_pie_html()

    from plotter_histogram import export_histogram_html
    export_histogram_html()

    from plotter_proportional_area import export_proportional_html
    export_proportional_html()

    from plotter_timeline import export_timeline_html
    export_timeline_html()

    from plotter_linear_regression import export_linear_regression_html
    export_linear_regression_html()

    # Deprecated
    # from plotter_fairometer import export_gauge_html
    # export_gauge_html()
