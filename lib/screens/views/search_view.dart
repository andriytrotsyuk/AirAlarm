import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/app_state.dart';
import '../../models/region.dart';

class SearchView extends StatefulWidget {
  const SearchView({super.key});

  @override
  State<SearchView> createState() => _SearchViewState();
}

class _SearchViewState extends State<SearchView> {
  final TextEditingController _searchController = TextEditingController();
  List<Region> _filteredRegions = [];

  void _filterRegions(String query, List<Region> allRegions) {
    if (query.isEmpty) {
      setState(() {
        _filteredRegions = allRegions;
      });
    } else {
      setState(() {
        _filteredRegions = allRegions
            .where((region) =>
                region.name.toLowerCase().contains(query.toLowerCase()))
            .toList();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);

    // If we haven't filtered yet (first build or after regions loaded), init with all
    if (_filteredRegions.isEmpty && _searchController.text.isEmpty) {
      _filteredRegions = appState.regions;
    }

    return Card(
      child: Column(
        children: [
          TextField(
            controller: _searchController,
            decoration: const InputDecoration(
              hintText: 'Пошук',
              prefixIcon: Icon(Icons.search),
            ),
            onChanged: (value) => _filterRegions(value, appState.regions),
            autofocus: true,
          ),
          const SizedBox(height: 8),
          Expanded(
            child: ListView.separated(
              itemCount: _filteredRegions.length,
              separatorBuilder: (context, index) => const Divider(),
              itemBuilder: (context, index) {
                final region = _filteredRegions[index];
                return ListTile(
                  title: Text(region.name),
                  subtitle:
                      region.display.isNotEmpty ? Text(region.display) : null,
                  onTap: () {
                    appState.setRegion(region.id);
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
