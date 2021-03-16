def network_graph(graph):
    
    pos=nx.get_node_attributes(graph,'pos')
    # set node positions
    pos = nx.spring_layout(graph)
#         pos = graphviz_layout(G, prog='circo')
    for node in graph.nodes():
        graph.nodes[node]['pos']= list(pos[node])

    pos=nx.get_node_attributes(graph,'pos')
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d


    p = nx.single_source_shortest_path_length(graph, ncenter)
    
#     print(etext)
    node_labels = list(graph.nodes)

        
    
    def make_edge(x, y, text, width):
        index = 0
        return  go.Scatter(x = x,
                           y = y,
                           line = dict(width = width
#                                        color = colors[index]
                                      ),
#                            marker=dict(color=colors[index]),
                           hoverinfo = 'text',
                           text = ([text]),
                           mode = 'lines')
    
    
        index = index + 1



#     # For each edge, make an edge_trace, append to list
    edge_trace = []
    for edge in graph.edges():

        if graph.edges()[edge]['Frequency'] > 0:
            char_1 = edge[0]
            char_2 = edge[1]

            x0, y0 = pos[char_1]
            x1, y1 = pos[char_2]

            text   = char_1 + '--' + char_2 + ': ' + str(graph.edges()[edge]['Frequency'])

            trace  = make_edge([x0, x1, None], [y0, y1, None], text,
                               0.1*graph.edges()[edge]['Frequency']**1.75)

            edge_trace.append(trace)

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=node_labels,
#         hovertext = labels,
        mode='markers + text ',
        hoverinfo='text',
        textfont=dict(
        family="sans serif",
#         size=17,
        color="#06D5FA",
#         line={'width': 10},
            
    ),
        
        marker=dict(
            showscale=False,
            
            colorscale='Rainbow',
            reversescale=False,
#             color=[color_map],
            size=30,
            colorbar=dict(
                thickness=15,
                title='',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=30))
    )
    for node in graph.nodes():
        x, y = graph.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(graph.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of relations: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies 
    node_trace.hovertext= node_text

    layout = go.Layout(
        title='Merchant relationship',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=1200,
        height=1200
    )


    fig = go.Figure(layout = layout)

    for trace in edge_trace:
        fig.add_trace(trace)

    fig.add_trace(node_trace)

    fig.update_layout(showlegend = False)

    fig.update_xaxes(showticklabels = False)

    fig.update_yaxes(showticklabels = False)

    return fig
